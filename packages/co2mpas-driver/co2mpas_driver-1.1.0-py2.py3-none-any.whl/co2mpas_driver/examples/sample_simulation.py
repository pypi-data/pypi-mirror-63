from os import path as osp, chdir
from co2mpas_driver.common import simulation_part as sp
import numpy as np
import matplotlib.pyplot as plt
from co2mpas_driver.common import curve_functions as mf
from co2mpas_driver.common import reading_n_organizing as rno
from co2mpas_driver.common import gear_functions as fg
from co2mpas_driver import dsp as driver

my_dir = osp.dirname(osp.abspath(__file__))
chdir(my_dir)


def simple_run():
    """
    Run simulation.

    :return:
    """
    # Vehicle databased based on the Euro Car Segment classification
    db_path = osp.abspath(osp.join(osp.dirname(my_dir + '/../'), 'db', 'EuroSegmentCar'))
    # A sample car id from the database
    car_id = 47844
    # The gear shifting style as described in the TRR paper.
    gs_style = 0.9

    # The desired speed
    vdes = 124/3.6

    # Current speed
    v_start = 0

    # The simulation step in seconds
    sim_step = 0.1

    # The driving style as described in the TRR paper.
    driver_style = 0.2

    # Duration of the simulation in seconds.
    duration = 100

    # sample time series
    times = np.arange(10, duration + sim_step, sim_step)

    # ******************************************************************************************
    driver_simulation_model = driver(dict(vehicle_id=car_id, inputs=dict(inputs=dict(
        gear_shifting_style=gs_style, desired_velocity=vdes,
        starting_velocity=v_start, driver_style=driver_style,
        sim_start=0, sim_step=sim_step, duration=duration))))[
        'outputs']['driver_simulation_model']

    res = {}
    for myt in times:
        if myt == times[0]:
            driver_simulation_model.reset(v_start)
            res = {'accel': [0], 'speed': [v_start],
                           'position': [0], 'gear': [0]}
            continue
        gear, next_velocity, acc, position = driver_simulation_model(sim_step, vdes)
        res['accel'].append(acc)
        res['speed'].append(next_velocity)
        res['gear'].append(gear)
        res['position'].append(position)

    plt.figure('Speed-Acceleration')
    plt.plot(res['speed'], res['accel'], 'x')
    plt.grid()
    # ******************************************************************************************
    '''import vehicle object, curves and gear shifting strategy'''
    db = rno.load_db_to_dictionary(db_path)

    # The vehicle specs as returned from the database
    selected_car = rno.get_vehicle_from_db(db, car_id, electric=True)

    '''
    The final acceleration curvers (Curves), the engine acceleration potential 
    curves (cs_acc_per_gear), before the calculation of the resistances and the 
    limitation due to max possible acceleration (friction) .
    '''
    Curves, Curves_dec, StartStop, gs = mf.get_ev_curve_main(selected_car)

    '''
        The difference betweeen "gear_4degree_curves_with_linear_gs" and 
        "gear_curves_n_gs_from_poly" is the
        computation of the engine acceleration potential curves
    '''
    # Curves, cs_acc_per_gear, StartStop, gs = mf.gear_curves_n_gs_from_
    # poly(selected_car, gs_style,4)

    '''Lists to gather simulation data'''
    Speeds = [v_start]
    Acceleration = [0]

    '''Initialize speed and gear'''
    speed = v_start
    '''
    Returns the gear that must be used and the clutch condition
    '''
    gear, gear_count = fg.gear_for_speed_profiles(gs, speed, 0, 0)
    gear_count = 0

    '''Core loop'''
    for t in times:
        speed, acceleration, gear, gear_count = sp.simulation_step_function(
            selected_car, speed, gear, gear_count, gs, Curves,
            vdes, driver_style, sim_step)

        '''Gather data'''
        Speeds.append(speed)
        Acceleration.append(acceleration)

    '''Plot'''
    plt.figure('Time-Speed')
    plt.plot(times, Speeds[1:])
    plt.grid()
    plt.figure('Speed-Acceleration')
    plt.plot(Speeds[1:], Acceleration[1:])
    plt.grid()
    plt.figure('Acceleration-Time')
    plt.plot(times, Acceleration[1:])
    plt.grid()

    plt.figure('Speed-Acceleration')
    for i, gear_curve in enumerate(Curves):
        sp_bins = np.arange(StartStop[0][i], StartStop[1][i] + 0.1, 0.1)
        accelerations = gear_curve(sp_bins)
        plt.plot(sp_bins, accelerations, 'k')
    # plt.grid()
    plt.show()


if __name__ == '__main__':
    simple_run()