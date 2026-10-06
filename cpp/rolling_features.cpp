#include <algorithm>
#include <cmath>
#include <cstddef>
#include <vector>

extern "C" {

// Optional native helper for high-volume rolling means. Python remains the default path.
void rolling_mean(const double* x, std::size_t n, std::size_t window, double* out) {
    if (!x || !out || n == 0 || window == 0) return;
    double sum = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        sum += x[i];
        if (i >= window) sum -= x[i - window];
        const std::size_t count = std::min(window, i + 1);
        out[i] = sum / static_cast<double>(count);
    }
}

}
