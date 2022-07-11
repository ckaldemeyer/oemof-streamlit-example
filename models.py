from unittest import result
import pyutilib.subprocess.GlobalData
import pandas as pd
from oemof.solph import (
    EnergySystem,
    Model,
    Flow,
    Bus,
    Sink,
    Source,
    GenericStorage,
    processing,
    views,
)


# this allows pyomo to run with streamlit/flask
# see:  https://stackoverflow.com/questions/57519088/
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def run_storage(
    data,
    bss_capacity=10000,
    bss_in=1000,
    bss_out=1000,
    bss_loss_rate=0.01,
    bss_eta_in=0.95,
    bss_eta_out=0.95,
    grid_max_power_consumption=1000000,
    grid_max_power_feedin=1000000,
    solver="cbc",
):

    data.index.freq = "1h"
    energy_system = EnergySystem(timeindex=data.index)

    b_el = Bus(label="b_el")

    bss = GenericStorage(
        label="bss",
        nominal_storage_capacity=bss_capacity,
        inputs={b_el: Flow(nominal_value=bss_in)},
        outputs={b_el: Flow(nominal_value=bss_out)},
        loss_rate=bss_loss_rate,
        inflow_conversion_factor=bss_eta_in,
        outflow_conversion_factor=bss_eta_out,
    )

    wind = Source(
        label="wind",
        outputs={
            b_el: Flow(
                max=data.loc[:, "Wind production (kWh)"],
                min=0,
                nominal_value=1,
                fixed=True,
            )
        },
    )

    grid_consumption = Source(
        label="grid_consumption",
        outputs={
            b_el: Flow(
                variable_costs=data.loc[:, "Electricity price (EUR/MWh)"],
                nominal_value=grid_max_power_consumption,
            )
        },
    )

    grid_feedin = Sink(
        label="grid_feedin",
        inputs={
            b_el: Flow(
                variable_costs=data.loc[:, "Electricity price (EUR/MWh)"] * -1,
                nominal_value=grid_max_power_feedin,
            )
        },
    )

    energy_system.add(
        b_el,
        bss,
        wind,
        grid_consumption,
        grid_feedin,
    )

    model = Model(energy_system)
    # model.write('test.lp', io_options={'symbolic_solver_labels': True})
    model.solve(solver=solver, solve_kwargs={"tee": False})

    results = processing.results(model)
    results = views.convert_keys_to_strings(results)
    results = views.node(results, "b_el")
    results = results["sequences"]
    results.insert(
        1,
        "Electricity price (EUR/MWh)",
        data.loc[:, "Electricity price (EUR/MWh)"],
    )
    columns = {
        "Electricity price (EUR/MWh)": "Electricity price (EUR/MWh)",
        (("wind", "b_el"), "flow"): "Wind",
        (
            ("b_el", "grid_feedin"),
            "flow",
        ): "Feedin",
        (("grid_consumption", "b_el"), "flow"): "Consumption",
    }
    results = results.rename(columns=columns)
    results = results.loc[:, list(columns.values())]

    results_storage = processing.results(model)
    results_storage = views.convert_keys_to_strings(results_storage)
    results_storage = views.node(results_storage, "bss")
    results_storage = results_storage["sequences"]
    columns = {
        (("bss", "None"), "storage_content"): "BSS (energy)",
        (("bss", "b_el"), "flow"): "BSS (out)",
        (("b_el", "bss"), "flow"): "BSS (in)",
    }
    results_storage = results_storage.rename(columns=columns)
    results_storage = results_storage.loc[:, list(columns.values())]

    results = pd.concat([results, results_storage], axis=1)
    results.loc[:, "BSS (power)"] = (
        results.loc[:, "BSS (out)"] - results.loc[:, "BSS (in)"]
    )

    return results
