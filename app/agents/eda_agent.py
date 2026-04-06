from app.tools.python_eda import analyze_data


def run_eda(data):
    return analyze_data(data)


# TEST
if __name__ == "__main__":
    from app.agents.collect_agent import collect_data

    data = collect_data("noise complaints")

    result = run_eda(data)

    print("EDA Agent Output:")
    print(result)