# Copyright (C) 2020  Oakes, Gregory <gregoryoakes@fastmail.com>
# Author: Oakes, Gregory <gregory.oakes@fastmail.com>
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

__version__ = "0.1.0"

from contextlib import contextmanager
from datetime import datetime
from json import loads
from os import path
from signal import SIGINT
from subprocess import PIPE, Popen

from serde import Model, fields
from serde.exceptions import ValidationError

try:
    from shutil import which
except ImportError:
    from backports.shutil_which import which


class IOStat(object):
    """Handler for the execution of an iostat subprocess and reporting of the stats."""

    def __init__(self, executable=None):
        """
        Arguments:
            **excutable** (Optional[str]) - The path to the iostat executable. If None,
            then the system `PATH` will be searched for one.
        """
        self.executable = executable or which("iostat")
        """The absolute path to the iostat executable which will be used."""
        self.stdout = None
        """The stdout of the most recent monitoring."""
        self.stderr = None
        """The stderr of the most recent monitoring."""
        self.stats = None
        """The statistics of the most recent monitoring.

        Structured as dictionary mapping "/dev/*" devices to a list of
        `iostat_context.StatRecord`s.
        """

    @contextmanager
    def monitor(self, devices=None, log_file=None, log_mode="w", interval=1):
        """Monitor the I/O statistics during the execution of the context.

        After exiting the context, `iostat_context.IOStat.stdout`,
        `iostat_context.IOStat.stderr`, and `iostat_context.IOStat.stats` will be
        populated from the iostat subprocesses output.

        Arguments:
            **devices** (Optional[Union[str, List[str]]]) - An optional list of devices
            or a single device to exclusively monitor. None means all.

            **log_file** (Optional[Union[str, file]]) - An optional file path or handle
            to which logs should be written in addition to parsing them internally.

            **log_mode** (str) - The mode with which log_file should be opened if
            log_file is a path.

            **interval** (int) - The interval at which statistics should be captured.
            Should not be less than 1.

        Raises:
            ValueError - interval is less than 1.
        """
        if interval < 1:
            raise ValueError(
                "Monitoring interval outside of allowed range: {}".format(interval)
            )
        # Ensure the file can be written to prior to allowing the context to execute.
        # This prevents long running IO from being performed and accidentally not
        # capturing the data afterwards.
        if isinstance(log_file, str):
            with open(log_file, log_mode):
                pass

        # Run iostat with extended output, device utilization, and timestamps in json
        # format.
        args = [self.executable, "-o", "JSON", "-xdt", str(interval)]
        if isinstance(devices, str):
            devices = [devices]
        if devices is not None:
            args += devices
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        try:
            yield
        finally:
            # Send SIGINT (ctrl-c) to let it safely shutdown and not output malformed
            # json.
            proc.send_signal(SIGINT)
            self.stdout, self.stderr = proc.communicate()
            if isinstance(self.stdout, bytes):
                self.stdout = self.stdout.decode()
            if isinstance(self.stderr, bytes):
                self.stderr = self.stderr.decode()
            self.stats = self.read_stats(self.stdout)
            if isinstance(log_file, str):
                with open(log_file, log_mode) as fh:
                    fh.write(self.stdout)
            elif log_file is not None:
                log_file.write(self.stdout)

    @classmethod
    def read_stats(cls, json_log):
        """Parse the stats from a json log.

        Return:
            If multiple hosts a present, then a mapping between each host and the
            statistic for each device will be returned. Otherwise, just the statistics
            for each device will be returned.
        """
        raw_hosts = loads(json_log).get("sysstat", {}).get("hosts", [])
        for host in raw_hosts:
            raw_stats = host.get("statistics", [])
            stats = {}
            for stat in raw_stats:
                timestamp = stat.get("timestamp")
                if timestamp is not None:
                    timestamp = datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p")
                for disk in stat.get("disk", []):
                    disk_device = disk.get("disk_device")
                    # Skip this record because it is invalid.
                    if disk_device is None:
                        continue
                    dev = path.join("/dev", disk_device)
                    if dev not in stats:
                        stats[dev] = []
                    record = StatRecord.from_dict(disk)
                    record.timestamp = timestamp
                    stats[dev].append(record)
            return stats
        return {}


class StatRecord(Model):
    """A single statistics record.

    Attributes:
        **disk_device** (str) - The device which was monitored without the leading
        "/dev/".

        **read_request_rate** (float) - The number (after merges) of read requests
        completed per second for the device.

        **write_request_rate** (float) - The number (after merges) of write requests
        completed per second for the device.

        **discard_request_rate** (float) - The number (after merges) of discard requests
        completed per second for the device.

        **flush_request_rate** (float) - The number (after merges) of flush requests
        completed per second for the device. This counts flush requests executed by
        disks. Flush requests are not tracked for partitions. Before  being  merged,
        flush operations are counted as writes.

        **read_rate** (float) - The  number of kilobytes read from the device per second.

        **write_rate** (float) - The number of kilobytes written to the device per second.

        **discard_rate** (float) - The number of kilobytes discarded for the device per
        second.

        **read_request_merge_rate** (float) - The number of read requests merged per
        second that were queued to the device.

        **write_request_merge_rate** (float) - The number of write requests merged per
        second that were queued to the device.

        **discard_request_merge_rate** (float) - The number of discard requests merged
        per second that were queued to the device.

        **discard_request_merge_rate** (float) - The number of discard requests merged
        per second that were queued to the device.

        **read_await** (float) - The average time (in milliseconds) for read requests
        issued to the device to be served. This includes the time spent by the requests
        in queue and the time spent servicing them.

        **write_await** (float) - The average time (in milliseconds) for write requests
        issued to the device to be served. This includes the time spent by the requests
        in queue and the time spent servicing them.

        **discard_await** (float) - The average time (in milliseconds) for discard
        requests issued to the device to be served. This includes the time spent by the
        requests in queue and the time spent servicing them.

        **flush_await** (float) - The average time (in milliseconds) for flush requests
        issued to the device to be served. The block layer combines flush requests and
        executes at most one at a time. Thus flush operations could be twice as long:
        Wait for current flush request, then execute it, then wait for the next one.

        **avg_read_request_size** (float) - The average size (in kilobytes) of the read
        requests that were issued to the device.

        **avg_write_request_size** (float) - The average size (in kilobytes) of the write
        requests that were issued to the device.

        **avg_discard_request_size** (float) - The average size (in kilobytes) of the
        discard requests that were issued to the device.

        **utilization** (float) - Percentage of elapsed time during which I/O requests
        were issued to the device (bandwidth utilization for the device). Device
        saturation occurs when this value is close to 100% for devices serving requests
        serially. But for devices serving requests in parallel, such as RAID arrays and
        modern SSDs, this number does not reflect their performance limits.

        **timestamp** (Optional[datetime]) - The moment during which this record was
        captured. This field is populated externally by `iostat_context.IOStat.monitor`
        as it is not strictly available in the json output of iostat, but is relevant to
        have directly associated with the record.
    """

    read_request_rate = fields.Float(rename="r/s")
    write_request_rate = fields.Float(rename="w/s")
    discard_request_rate = fields.Float(rename="d/s")
    flust_request_rate = fields.Float(rename="f/s")
    read_rate = fields.Float(rename="rkB/s")
    write_rate = fields.Float(rename="wkB/s")
    discard_rate = fields.Float(rename="dkB/s")
    read_request_merge_rate = fields.Float(rename="rrqm/s")
    write_request_merge_rate = fields.Float(rename="wrqm/s")
    discard_request_merge_rate = fields.Float(rename="drqm/s")
    read_await = fields.Float(rename="r_await")
    write_await = fields.Float(rename="w_await")
    discard_await = fields.Float(rename="d_await")
    flush_await = fields.Float(rename="f_await")
    avg_read_request_size = fields.Float(rename="rareq-sz")
    avg_write_request_size = fields.Float(rename="wareq-sz")
    avg_discard_request_size = fields.Float(rename="dareq-sz")
    utilization = fields.Float(rename="util")

    # Try to deserialize both but don't expect them. The class's validate function will
    # handle ensuring at least one of these exists.
    _aqu_sz = fields.Optional(fields.Float(), rename="aqu-sz")
    _avgqu_sz = fields.Optional(fields.Float(), rename="avgqu-sz")

    @property
    def avg_queue_length(self):
        """Return the average queue length of requests that were issued to the device."""
        if self._aqu_sz is not None:
            # Return new name.
            return self._aqu_sz
        # Return old name.
        return self._avgqu_sz

    def __init__(self, *args, **kwargs):
        super(StatRecord, self).__init__(*args, **kwargs)
        self.timestamp = None

    def validate(self):
        """Verify the resulting model is valid."""
        if self._aqu_sz is None and self._avgqu_sz is None:
            raise ValidationError("Exected field 'average_queue_length'.")
