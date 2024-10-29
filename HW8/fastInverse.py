import struct
import numpy as np
import time
import matplotlib.pyplot as plt

# Fast Inverse Square Root function (based on Quake III Arena)
def fast_inverse_sqrt(x):
    x = np.float32(x)
    i = struct.unpack('i', struct.pack('f', x))[0]  # Get raw bits representation of the float
    i = 0x5f3759df - (i >> 1)  # Apply the magic number
    y = struct.unpack('f', struct.pack('i', i))[0]  # Reconstruct float from bits
    y = y * (1.5 - 0.5 * x * y * y)  # One iteration of Newton's method
    return y

# Standard library function for inverse square root
def std_inverse_sqrt(x):
    return 1 / np.sqrt(x)

# Performance comparison
def compare_performance(input_size=10000):
    x_values = np.random.random(input_size).astype(np.float32) * 100  # Generate random floats

    # Fast inverse square root timing
    start_time = time.perf_counter()
    fast_results = [fast_inverse_sqrt(x) for x in x_values]
    fast_duration = time.perf_counter() - start_time

    # Standard library inverse square root timing
    start_time = time.perf_counter()
    std_results = [std_inverse_sqrt(x) for x in x_values]
    std_duration = time.perf_counter() - start_time

    return fast_duration, std_duration, fast_results, std_results, x_values

# Running performance comparison across different input sizes
input_sizes = [100, 1000, 5000, 10000, 20000, 50000]
fast_times = []
std_times = []

for size in input_sizes:
    fast_time, std_time, _, _, _ = compare_performance(size)
    fast_times.append(fast_time)
    std_times.append(std_time)

# Now running for the default input size of 10,000 for accuracy comparison
input_size = 10000
fast_time, std_time, fast_results, std_results, x_values = compare_performance(input_size)

# Accuracy comparison
fast_results = np.array(fast_results)
std_results = np.array(std_results)
relative_error = np.abs((fast_results - std_results) / std_results)
max_relative_error = np.max(relative_error)
mean_relative_error = np.mean(relative_error)
median_relative_error = np.median(relative_error)

# Plotting both graphs in the same figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Time Performance Plot
ax1.plot(input_sizes, fast_times, label='Fast Inverse Sqrt', marker='o')
ax1.plot(input_sizes, std_times, label='Standard Inverse Sqrt', marker='x')
ax1.set_xlabel('Input Size')
ax1.set_ylabel('Execution Time (seconds)')
ax1.set_title('Execution Time Comparison for Different Input Sizes')
ax1.legend()
ax1.grid(True)

# Relative Error Histogram
ax2.hist(relative_error, bins=50, edgecolor='black')
ax2.set_xlabel('Relative Error')
ax2.set_ylabel('Frequency')
ax2.set_title('Distribution of Relative Errors')
ax2.grid(True)

plt.tight_layout()
plt.show()

# Time Performance Summary
print(f"Execution Time for Input Size {input_size}:")
print(f"Fast Inverse Sqrt Time (s): {fast_time:.6f}")
print(f"Standard Inverse Sqrt Time (s): {std_time:.6f}")

# Accuracy Analysis
print("\nAccuracy Analysis:")
print(f"Maximum Relative Error: {max_relative_error:.8f}")
print(f"Mean Relative Error: {mean_relative_error:.8f}")
print(f"Median Relative Error: {median_relative_error:.8f}")

# Additional Analysis
print("\nAdditional Analysis:")
print(f"Standard method is on average {fast_time / std_time:.2f} times faster than the fast method")
#print(f"Fast method is on average {fast_time / std_time:.2f} times faster than the standard method")
print(f"Percentage of results with relative error < 1%: {np.mean(relative_error < 0.01) * 100:.2f}%")
print(f"Percentage of results with relative error < 0.1%: {np.mean(relative_error < 0.001) * 100:.2f}%")
