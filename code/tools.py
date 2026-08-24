import math

def rule_of_72(rate=None, time=None):

    if (rate is None and time is None) or (rate is not None and time is not None):
        raise ValueError("Provide exactly one parameter: rate OR time.")

    if rate is not None:
        if rate <= 0:
            raise ValueError("Rate must be greater than 0.")
        years = 72.0 / rate
        return {"rate_pct": rate, "years": years}

    if time is not None:
        if time <= 0:
            raise ValueError("Time must be greater than 0.")
        rate_pct = 72.0 / time
        return {"time_years": time, "rate_pct": rate_pct}


def compare_rates(rates):
    result = []
    for r in rates:
        if r <= 0:
            result.append({"rate_pct": r, "error": "rate must be > 0"})
        else:
            years = 72.0 / r
            result.append({"rate_pct": r, "doubling_years": years})
    return result


def growth_over_time(principal, rate_pct, years):
    result = []
    rate = rate_pct / 100.0
    for y in range(years + 1):
        value = principal * ((1 + rate) ** y)
        result.append((y, value))
    return result


def plot_growth(principal, rate_pct, years, save_path=None):
    try:
        import matplotlib.pyplot as plt
    except:
        raise RuntimeError("matplotlib is required for plotting. Install it with 'pip install matplotlib'.")

    data = growth_over_time(principal, rate_pct, years)
    xs = [t for t, _ in data]
    ys = [v for _, v in data]

    plt.figure()
    plt.plot(xs, ys)
    plt.title(f"Growth: {principal} at {rate_pct}%")
    plt.xlabel("Years")
    plt.ylabel("Value")
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
