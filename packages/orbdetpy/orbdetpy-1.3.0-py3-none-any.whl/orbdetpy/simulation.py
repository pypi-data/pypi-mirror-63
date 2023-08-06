# simulation.py - Measurement simulation functions.
# Copyright (C) 2019-2020 University of Texas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from traceback import format_exc
from orbdetpy import write_output_file
from orbdetpy.rpc import simulation_pb2_grpc
from orbdetpy.rpc.server import RemoteServer
from orbdetpy.rpc.tools import build_settings, convert_measurements

def simulate_measurements(config, output_file = None):
    """ Simulates measurement data given a configuration.

    Args:
        config: Simulation configuration (Dictionary, file name, text
                file-like object, or JSON encoded string).
        output_file: If specified, the measurements will be written to
                     the file name or text file-like object given.

    Returns:
        Simulated measurements.
    """

    if (isinstance(config, list)):
        sim_output = []
    else:
        sim_output = None
        config = [config]
    if (output_file and not isinstance(output_file, list)):
        output_file = [output_file]

    with RemoteServer.channel() as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        requests = [stub.simulateMeasurements.future(build_settings(c))
                    for c in config]

        for idx, req in enumerate(requests):
            try:
                sim_data = convert_measurements(req.result().array)
            except Exception as exc:
                sim_data = format_exc()

            if (sim_output is None):
                sim_output = sim_data
            else:
                sim_output.append(sim_data)
            if (output_file):
                write_output_file(output_file[idx], sim_data)

    return(sim_output)
