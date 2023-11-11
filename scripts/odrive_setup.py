import odrive
import time
import odrive.enums
import fibre

print("ODRIVE MAGIC CONFIGURATOR BY RAUL ARCOS")
try:
    odrv0 = odrive.find_any()
    print("Odrive Encontrada! Serial number: {}".format(odrv0.serial_number))
except:
    print("No Odrive found!")

print("Aplicando configuración Inicial")
odrv0.axis0.motor.config.pole_pairs = 15
odrv0.axis0.motor.config.resistance_calib_max_voltage = 12
odrv0.axis0.motor.config.requested_current_range = 15 #Requires config save and reboot
odrv0.axis0.motor.config.calibration_current=12
odrv0.axis0.motor.config.motor_type = odrive.enums.MOTOR_TYPE_HIGH_CURRENT
odrv0.axis0.motor.config.current_control_bandwidth = 100
odrv0.axis0.motor.config.torque_constant = 8.27 / 16
odrv0.axis0.encoder.config.mode = odrive.enums.ENCODER_MODE_HALL
odrv0.axis0.encoder.config.cpr = 90
odrv0.axis0.encoder.config.bandwidth = 100
odrv0.axis0.controller.config.pos_gain = 1
odrv0.axis0.controller.config.vel_gain = 0.02 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr
odrv0.axis0.controller.config.vel_integrator_gain = 0.1 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr
odrv0.axis0.controller.config.vel_limit = 10
odrv0.axis0.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis1.motor.config.pole_pairs = 15
odrv0.axis1.motor.config.resistance_calib_max_voltage = 12
odrv0.axis1.motor.config.requested_current_range = 15 #Requires config save and reboot
odrv0.axis1.motor.config.calibration_current=12
odrv0.axis1.motor.config.motor_type = odrive.enums.MOTOR_TYPE_HIGH_CURRENT
odrv0.axis1.motor.config.current_control_bandwidth = 100
odrv0.axis1.motor.config.torque_constant = 8.27 / 16
odrv0.axis1.encoder.config.mode = odrive.enums.ENCODER_MODE_HALL
odrv0.axis1.encoder.config.cpr = 90
odrv0.axis1.encoder.config.bandwidth = 100
odrv0.axis1.controller.config.pos_gain = 1
odrv0.axis1.controller.config.vel_gain = 0.02 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr
odrv0.axis1.controller.config.vel_integrator_gain = 0.1 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr
odrv0.axis1.controller.config.vel_limit = 10
odrv0.axis1.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL
odrv0.save_configuration()
try:
    odrv0.reboot()
except fibre.libfibre.ObjectLostError:
    print("Configuración Inicial Aplicada!")
    time.sleep(2)
    try:
        odrv0 = odrive.find_any()
        print("Odrive Encontrada! Serial number: {}".format(odrv0.serial_number))
    except:
        print("No Odrive found!")

print("Calibrando Ruedas...NO TOCAR!")
odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
time.sleep(20)
print("Ruedas Calibradas! :D")
print("Aplicando úlimas configuraciones...")
odrv0.axis0.motor.config.pre_calibrated = True
odrv0.axis1.motor.config.pre_calibrated = True
odrv0.axis0.encoder.config.pre_calibrated = True
odrv0.axis1.encoder.config.pre_calibrated = True

odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL

print("Guardando configuración...")
odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_IDLE
odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_IDLE
odrv0.axis0.config.startup_closed_loop_control = True
odrv0.axis1.config.startup_closed_loop_control = True
odrv0.save_configuration()
try:
    odrv0.reboot()
except fibre.libfibre.ObjectLostError:
    print("CONFIGURACIÓN COMPLETADA! :)")
    time.sleep(2)