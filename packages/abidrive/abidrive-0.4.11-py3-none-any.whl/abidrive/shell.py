
import sys
import platform
import threading
import fibre
import abidrive
import abidrive.enums
from abidrive.utils import start_liveplotter, dump_errors
#from abidrive.enums import * # pylint: disable=W0614

def print_banner():
    print('Please connect your AbiDrive.')
    print('You can also type help() or quit().')

def print_help(args, have_devices):
    print('')
    if have_devices:
        print('Connect your AbiDrive to {} and power it up.'.format(args.path))
        print('After that, the following message should appear:')
        print('  "Connected to AbiDrive [serial number] as abidrv0"')
        print('')
        print('Once the AbiDrive is connected, type "abidrv0." and press <tab>')
    else:
        print('Type "abidrv0." and press <tab>')
    print('This will present you with all the properties that you can reference')
    print('')
    print('For example: "abidrv0.motor0.encoder.pos_estimate"')
    print('will print the current encoder position on motor 0')
    print('and "abidrv0.motor0.pos_setpoint = 10000"')
    print('will send motor0 to 10000')
    print('')


interactive_variables = {}

discovered_devices = []

def did_discover_device(abidrive, logger, app_shutdown_token):
    """
    Handles the discovery of new devices by displaying a
    message and making the device available to the interactive
    console
    """
    serial_number = abidrive.serial_number if hasattr(abidrive, 'serial_number') else "[unknown serial number]"
    if serial_number in discovered_devices:
        verb = "Reconnected"
        index = discovered_devices.index(serial_number)
    else:
        verb = "Connected"
        discovered_devices.append(serial_number)
        index = len(discovered_devices) - 1
    interactive_name = "abidrv" + str(index)

    # Publish new AbiDrive to interactive console
    interactive_variables[interactive_name] = abidrive
    globals()[interactive_name] = abidrive # Add to globals so tab complete works
    logger.notify("{} to AbiDrive {:012X} as {}".format(verb, serial_number, interactive_name))

    # Subscribe to disappearance of the device
    abidrive.__channel__._channel_broken.subscribe(lambda: did_lose_device(interactive_name, logger, app_shutdown_token))

def did_lose_device(interactive_name, logger, app_shutdown_token):
    """
    Handles the disappearance of a device by displaying
    a message.
    """
    if not app_shutdown_token.is_set():
        logger.warn("Oh no {} disappeared".format(interactive_name))

def launch_shell(args, logger, app_shutdown_token):
    """
    Launches an interactive python or IPython command line
    interface.
    As AbiDrives are connected they are made available as
    "abidrv0", "abidrv1", ...
    """

    interactive_variables = {
        'start_liveplotter': start_liveplotter,
        'dump_errors': dump_errors
    }

    # Expose all enums from abidrive.enums
    interactive_variables.update({k: v for (k, v) in abidrive.enums.__dict__.items() if not k.startswith("_")})

    fibre.launch_shell(args,
                       interactive_variables,
                       print_banner, print_help,
                       logger, app_shutdown_token,
                       branding_short="abidrv", branding_long="AbiDrive")
