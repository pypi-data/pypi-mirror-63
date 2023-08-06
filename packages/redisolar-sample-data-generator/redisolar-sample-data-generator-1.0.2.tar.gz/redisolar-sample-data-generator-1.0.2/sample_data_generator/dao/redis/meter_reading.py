from sample_data_generator.models import MeterReading
from sample_data_generator.dao.base import MeterReadingDaoBase
from sample_data_generator.dao.redis import CapacityReportDaoRedis
from sample_data_generator.dao.redis import FeedDaoRedis
from sample_data_generator.dao.redis import MetricDaoRedis
from sample_data_generator.dao.redis import SiteStatsDaoRedis
from sample_data_generator.dao.redis.base import RedisDaoBase


class MeterReadingDaoRedis(MeterReadingDaoBase, RedisDaoBase):
    """MeterReadingDaoRedis persists MeterReading models to Redis."""
    def add(self, meter_reading: MeterReading, **kwargs) -> None:
        MetricDaoRedis(self.redis).insert(meter_reading, **kwargs)
        SiteStatsDaoRedis(self.redis).update(meter_reading, **kwargs)
        CapacityReportDaoRedis(self.redis).update(meter_reading, **kwargs)
        FeedDaoRedis(self.redis).insert(meter_reading, **kwargs)
