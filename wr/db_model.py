import peewee as pw

db = pw.SqliteDatabase('weather.sqlite')


class RDMWeatherData(pw.Model):
    timestamp = pw.IntegerField(primary_key=True)
    temperature = pw.FloatField()
    humidity = pw.FloatField()
    pressure = pw.FloatField()

    class Meta:
        database = db


class DWDWeatherData(pw.Model):
    timestamp = pw.IntegerField(primary_key=True)
    temperature = pw.FloatField()
    humidity = pw.FloatField()
    pressure = pw.FloatField()

    class Meta:
        database = db