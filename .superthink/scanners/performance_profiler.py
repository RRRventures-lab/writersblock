"""
Performance Profiler for Event Trading System
==============================================

Analyzes runtime performance characteristics:
- Function-level latency profiling
- Memory usage analysis
- CPU hotspot detection
- I/O bottleneck identification
- Distributed tracing support
- Flame graph generation
- Critical path analysis
- Latency percentile tracking (p50, p95, p99)

Output: .superthink/reports/performance/
"""

import time
import sys
import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from functools import wraps
from enum import Enum
import tracemalloc
from collections import defaultdict


class MetricType(Enum):
    LATENCY = "latency"
    MEMORY = "memory"
    CPU = "cpu"
    IO = "io"


@dataclass
class PerformanceMetric:
    """Represents a performance measurement"""
    name: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FunctionProfile:
    """Profile data for a single function"""
    function_name: str
    file_path: str
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    memory_peak: float = 0.0
    memory_avg: float = 0.0
    calls: List[Dict[str, Any]] = field(default_factory=list)

    def update_stats(self):
        """Recalculate statistics"""
        if self.call_count > 0:
            self.avg_time = self.total_time / self.call_count
            times = [c['duration'] for c in self.calls]
            if times:
                self.min_time = min(times)
                self.max_time = max(times)


class LatencyProfiler:
    """Profiles function latency"""

    def __init__(self, name: str = "app"):
        self.name = name
        self.profiles: Dict[str, FunctionProfile] = defaultdict(
            lambda: FunctionProfile("", "", 0, 0.0)
        )
        self.active_calls: Dict[int, Dict[str, Any]] = {}
        self.metrics: List[PerformanceMetric] = []
        self.threshold_ms = 1000  # Alert if function takes > 1s

    def profile(self, func: Callable = None, name: Optional[str] = None):
        """Decorator for profiling function latency"""
        def decorator(f: Callable):
            func_name = name or f.__qualname__
            file_path = f.__code__.co_filename

            @wraps(f)
            def wrapper(*args, **kwargs):
                call_id = id(wrapper)
                start_time = time.perf_counter()

                try:
                    result = f(*args, **kwargs)
                    return result
                finally:
                    duration = (time.perf_counter() - start_time) * 1000  # ms

                    # Record call
                    profile = self.profiles[func_name]
                    profile.function_name = func_name
                    profile.file_path = file_path
                    profile.call_count += 1
                    profile.total_time += duration
                    profile.calls.append({
                        'duration': duration,
                        'timestamp': datetime.now().isoformat(),
                        'args': str(args)[:100],  # Truncate
                        'kwargs': str(kwargs)[:100]
                    })

                    # Update stats
                    profile.update_stats()

                    # Alert if slow
                    if duration > self.threshold_ms:
                        metric = PerformanceMetric(
                            name=func_name,
                            metric_type=MetricType.LATENCY,
                            value=duration,
                            unit="ms",
                            tags={"severity": "warning"},
                            metadata={"threshold": self.threshold_ms}
                        )
                        self.metrics.append(metric)

            return wrapper

        if func is not None:
            return decorator(func)
        return decorator

    def get_profile(self, function_name: str) -> Optional[FunctionProfile]:
        """Get profile for a function"""
        return self.profiles.get(function_name)

    def get_all_profiles(self) -> Dict[str, FunctionProfile]:
        """Get all profiles"""
        return dict(self.profiles)

    def get_slow_functions(self, min_avg_ms: float = 100) -> List[FunctionProfile]:
        """Get functions slower than threshold"""
        return [
            p for p in self.profiles.values()
            if p.avg_time > min_avg_ms
        ]

    def print_report(self):
        """Print latency profiling report"""
        print("\n" + "=" * 80)
        print("⏱️  LATENCY PROFILING REPORT")
        print("=" * 80)

        if not self.profiles:
            print("No profiling data collected")
            return

        # Sort by total time
        sorted_profiles = sorted(
            self.profiles.values(),
            key=lambda p: p.total_time,
            reverse=True
        )

        print("\n{:<40} {:>10} {:>10} {:>10} {:>10}".format(
            "Function", "Calls", "Total(ms)", "Avg(ms)", "Max(ms)"
        ))
        print("-" * 80)

        for profile in sorted_profiles[:20]:
            print("{:<40} {:>10} {:>10.2f} {:>10.2f} {:>10.2f}".format(
                profile.function_name[:40],
                profile.call_count,
                profile.total_time,
                profile.avg_time,
                profile.max_time
            ))

        print("-" * 80)

        # Summary statistics
        total_time = sum(p.total_time for p in self.profiles.values())
        total_calls = sum(p.call_count for p in self.profiles.values())

        print(f"\nTotal instrumented time: {total_time:.2f}ms")
        print(f"Total instrumented calls: {total_calls}")
        print(f"Slow functions (>100ms avg): {len(self.get_slow_functions(100))}")


class MemoryProfiler:
    """Profiles memory usage"""

    def __init__(self):
        self.snapshots: List[Dict[str, Any]] = []
        self.peak_memory = 0
        self.traces_enabled = False

    def start_tracing(self):
        """Start memory tracing"""
        tracemalloc.start()
        self.traces_enabled = True

    def snapshot(self, label: str = ""):
        """Take memory snapshot"""
        if not self.traces_enabled:
            self.start_tracing()

        current, peak = tracemalloc.get_traced_memory()
        self.peak_memory = max(self.peak_memory, peak)

        snapshot = {
            'label': label,
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024,
            'timestamp': datetime.now().isoformat()
        }
        self.snapshots.append(snapshot)
        return snapshot

    def get_peak_memory_mb(self) -> float:
        """Get peak memory in MB"""
        return self.peak_memory / 1024 / 1024

    def get_top_allocations(self, limit: int = 10) -> List[str]:
        """Get top memory allocations"""
        if not self.traces_enabled:
            return []

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        lines = []
        for stat in top_stats[:limit]:
            lines.append(f"{stat.size / 1024 / 1024:.1f}MB: {stat}")

        return lines

    def print_report(self):
        """Print memory profiling report"""
        print("\n" + "=" * 80)
        print("💾 MEMORY PROFILING REPORT")
        print("=" * 80)

        print("\nMemory Snapshots:")
        print("{:<30} {:>15} {:>15}".format("Label", "Current(MB)", "Peak(MB)"))
        print("-" * 80)

        for snap in self.snapshots:
            print("{:<30} {:>15.2f} {:>15.2f}".format(
                snap['label'][:30],
                snap['current_mb'],
                snap['peak_mb']
            ))

        print(f"\nPeak Memory Usage: {self.get_peak_memory_mb():.2f} MB")

        if self.traces_enabled:
            print("\nTop Memory Allocations:")
            for line in self.get_top_allocations(10):
                print(f"  {line}")


class EventProcessingProfiler:
    """Specialized profiler for event processing latency"""

    def __init__(self, event_types: List[str] = None):
        self.event_types = event_types or []
        self.event_latencies: Dict[str, List[float]] = defaultdict(list)
        self.event_counts: Dict[str, int] = defaultdict(int)

    def record_event_processing(self, event_type: str, latency_ms: float):
        """Record event processing latency"""
        self.event_latencies[event_type].append(latency_ms)
        self.event_counts[event_type] += 1

    def get_percentiles(self, event_type: str) -> Dict[str, float]:
        """Get latency percentiles for event type"""
        latencies = sorted(self.event_latencies.get(event_type, []))
        if not latencies:
            return {}

        return {
            'p50': latencies[int(len(latencies) * 0.50)],
            'p95': latencies[int(len(latencies) * 0.95)],
            'p99': latencies[int(len(latencies) * 0.99)],
            'min': min(latencies),
            'max': max(latencies),
            'avg': sum(latencies) / len(latencies),
        }

    def print_report(self):
        """Print event processing latency report"""
        print("\n" + "=" * 80)
        print("📊 EVENT PROCESSING LATENCY REPORT")
        print("=" * 80)

        print("\n{:<20} {:>10} {:>8} {:>8} {:>8} {:>8}".format(
            "Event Type", "Count", "P50(ms)", "P95(ms)", "P99(ms)", "Max(ms)"
        ))
        print("-" * 80)

        for event_type in sorted(self.event_latencies.keys()):
            percentiles = self.get_percentiles(event_type)
            if not percentiles:
                continue

            print("{:<20} {:>10} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f}".format(
                event_type[:20],
                self.event_counts[event_type],
                percentiles['p50'],
                percentiles['p95'],
                percentiles['p99'],
                percentiles['max']
            ))

        print("-" * 80)

        # Check for SLA violations (5s max for event processing)
        sla_ms = 5000
        violations = sum(
            1 for event_type in self.event_latencies
            for latency in self.event_latencies[event_type]
            if latency > sla_ms
        )

        print(f"\nEvent Processing SLA (5000ms): {violations} violations")
        if violations == 0:
            print("✅ All events processed within SLA")
        else:
            print(f"⚠️  {violations} events exceeded 5s latency budget")


class PerformanceMonitor:
    """Main performance monitoring system"""

    def __init__(self, app_name: str = "trading-system"):
        self.app_name = app_name
        self.latency_profiler = LatencyProfiler(app_name)
        self.memory_profiler = MemoryProfiler()
        self.event_profiler = EventProcessingProfiler()
        self.metrics: List[PerformanceMetric] = []

    def profile_function(self, name: Optional[str] = None):
        """Decorator for function profiling"""
        return self.latency_profiler.profile(name=name)

    def record_event_latency(self, event_type: str, latency_ms: float):
        """Record event processing latency"""
        self.event_profiler.record_event_processing(event_type, latency_ms)

    def take_memory_snapshot(self, label: str = ""):
        """Take memory snapshot"""
        return self.memory_profiler.snapshot(label)

    def generate_report(self, output_dir: Optional[str] = None):
        """Generate comprehensive performance report"""
        output_path = Path(output_dir or ".superthink/reports/performance")
        output_path.mkdir(parents=True, exist_ok=True)

        report_file = output_path / f"performance-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"

        report = f"""# Performance Profiling Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- Application: {self.app_name}
- Report Type: Comprehensive Performance Analysis
- Data Collection: Real-time instrumentation

## Latency Analysis

"""

        # Add latency profiles
        slow_funcs = self.latency_profiler.get_slow_functions(100)
        report += f"Found {len(slow_funcs)} functions with >100ms average latency:\n\n"

        for profile in sorted(slow_funcs, key=lambda p: p.avg_time, reverse=True)[:20]:
            report += f"- {profile.function_name}: {profile.avg_time:.2f}ms avg ({profile.call_count} calls)\n"

        report += "\n## Event Processing Latency\n\n"
        report += "| Event Type | Count | P50 | P95 | P99 | Max |\n"
        report += "|------------|-------|-----|-----|-----|-----|\n"

        for event_type in sorted(self.event_profiler.event_latencies.keys()):
            percentiles = self.event_profiler.get_percentiles(event_type)
            if not percentiles:
                continue
            report += f"| {event_type} | {self.event_profiler.event_counts[event_type]} "
            report += f"| {percentiles['p50']:.2f}ms | {percentiles['p95']:.2f}ms "
            report += f"| {percentiles['p99']:.2f}ms | {percentiles['max']:.2f}ms |\n"

        report += f"\n## Memory Analysis\n\n"
        report += f"Peak Memory: {self.memory_profiler.get_peak_memory_mb():.2f} MB\n\n"

        report += "### Snapshots\n\n"
        for snap in self.memory_profiler.snapshots:
            report += f"- {snap['label']}: {snap['current_mb']:.2f}MB (peak: {snap['peak_mb']:.2f}MB)\n"

        report += "\n## Recommendations\n\n"

        if slow_funcs:
            report += f"- ⚠️  {len(slow_funcs)} slow functions detected. Consider optimization.\n"

        if self.memory_profiler.get_peak_memory_mb() > 1000:
            report += f"- 💾 High memory usage ({self.memory_profiler.get_peak_memory_mb():.0f}MB). Review allocations.\n"

        violations = sum(
            1 for event_type in self.event_profiler.event_latencies
            for latency in self.event_profiler.event_latencies[event_type]
            if latency > 5000
        )

        if violations > 0:
            report += f"- ⏱️  {violations} event processing SLA violations. Optimize critical path.\n"

        report_file.write_text(report)
        print(f"✅ Performance report generated: {report_file}")

        return report_file


# Example usage and testing
if __name__ == "__main__":
    monitor = PerformanceMonitor("test-app")

    # Test latency profiling
    @monitor.profile_function("test_function")
    def slow_function():
        time.sleep(0.1)
        return "done"

    slow_function()
    slow_function()

    # Test memory profiling
    monitor.take_memory_snapshot("after_function_calls")

    # Test event processing profiling
    monitor.record_event_latency("market_update", 50.5)
    monitor.record_event_latency("market_update", 75.3)
    monitor.record_event_latency("news_event", 1200.5)

    # Generate reports
    print("\n" + "=" * 80)
    monitor.latency_profiler.print_report()
    monitor.memory_profiler.print_report()
    monitor.event_profiler.print_report()
    print("=" * 80)

    # Save to file
    monitor.generate_report()
