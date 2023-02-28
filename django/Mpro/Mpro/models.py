from django.db import models


class GdpEconomicGrowthRate(models.Model):
    year = models.IntegerField(primary_key=True)
    nominal_gdp = models.TextField(db_column='nominal_GDP', blank=True, null=True)  # Field name made lowercase.
    economic_growth_rate = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GDP_economic_growth_rate'


class GniPerCapita(models.Model):
    year = models.IntegerField(primary_key=True)
    real_gni_per_capita = models.TextField(db_column='real_GNI_per_capita', blank=True, null=True)  # Field name made lowercase.
    real_gni_growth_rate = models.TextField(db_column='real_GNI_growth_rate', blank=True, null=True)  # Field name made lowercase.
    nominal_gni_per_capita = models.TextField(db_column='nominal_GNI_per_capita', blank=True, null=True)  # Field name made lowercase.
    nominal_gni_growth_rate = models.TextField(db_column='nominal_GNI_growth_rate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GNI_per_capita'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BusinessLoanInterest(models.Model):
    bank = models.CharField(primary_key=True, max_length=20)
    number_2017 = models.FloatField(db_column='2017')  # Field renamed because it wasn't a valid Python identifier.
    number_2018 = models.FloatField(db_column='2018')  # Field renamed because it wasn't a valid Python identifier.
    number_2019 = models.FloatField(db_column='2019')  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'business_loan_interest'


class ConsumerPriceIndex(models.Model):
    years = models.CharField(primary_key=True, max_length=20)
    cpi = models.FloatField(db_column='CPI')  # Field name made lowercase.
    cpi_inflation = models.FloatField(db_column='CPI_inflation')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consumer_price_index'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RegionalPopulation(models.Model):
    year = models.IntegerField(primary_key=True)
    population = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'regional_population'


class SeoulCommercialArea(models.Model):
    gu_name = models.CharField(db_column='GU_NAME', primary_key=True, max_length=20)  # Field name made lowercase.
    foot_traffic = models.IntegerField(db_column='FOOT_TRAFFIC')  # Field name made lowercase.
    population = models.IntegerField(db_column='POPULATION')  # Field name made lowercase.
    workers = models.IntegerField(db_column='WORKERS')  # Field name made lowercase.
    index_year = models.IntegerField(db_column='INDEX_YEAR')  # Field name made lowercase.
    density = models.IntegerField(db_column='DENSITY')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seoul_commercial_area'
        unique_together = (('gu_name', 'index_year'),)


class SeoulMetroStation(models.Model):
    station_name = models.CharField(primary_key=True, max_length=20)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        managed = False
        db_table = 'seoul_metro_station'


class SeoulRestaurant(models.Model):
    mgtno = models.CharField(db_column='MGTNO', primary_key=True, max_length=30)  # Field name made lowercase.
    bplcnm = models.TextField(db_column='BPLCNM', blank=True, null=True)  # Field name made lowercase.
    uptaenm = models.CharField(db_column='UPTAENM', max_length=15)  # Field name made lowercase.
    sitewhladdr = models.TextField(db_column='SITEWHLADDR', blank=True, null=True)  # Field name made lowercase.
    faciltotscp = models.FloatField(db_column='FACILTOTSCP', blank=True, null=True)  # Field name made lowercase.
    dtlstatenm = models.TextField(db_column='DTLSTATENM', blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='YEAR', max_length=10)  # Field name made lowercase.
    month = models.CharField(db_column='MONTH', max_length=10)  # Field name made lowercase.
    day = models.CharField(db_column='DAY', max_length=10)  # Field name made lowercase.
    x = models.TextField(db_column='X', blank=True, null=True)  # Field name made lowercase.
    y = models.TextField(db_column='Y', blank=True, null=True)  # Field name made lowercase.
    franchise = models.IntegerField()
    gu = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'seoul_restaurant'


class SeoulStoreDataPreProc(models.Model):
    index = models.BigIntegerField(primary_key=True)
    bizesnm = models.TextField(db_column='bizesNm', blank=True, null=True)  # Field name made lowercase.
    indsmclscd = models.TextField(db_column='indsMclsCd', blank=True, null=True)  # Field name made lowercase.
    indsmclsnm = models.TextField(db_column='indsMclsNm', blank=True, null=True)  # Field name made lowercase.
    indssclscd = models.TextField(db_column='indsSclsCd', blank=True, null=True)  # Field name made lowercase.
    indssclsnm = models.TextField(db_column='indsSclsNm', blank=True, null=True)  # Field name made lowercase.
    ctprvncd = models.TextField(db_column='ctprvnCd', blank=True, null=True)  # Field name made lowercase.
    ctprvnnm = models.TextField(db_column='ctprvnNm', blank=True, null=True)  # Field name made lowercase.
    signgucd = models.TextField(db_column='signguCd', blank=True, null=True)  # Field name made lowercase.
    signgunm = models.TextField(db_column='signguNm', blank=True, null=True)  # Field name made lowercase.
    adongcd = models.TextField(db_column='adongCd', blank=True, null=True)  # Field name made lowercase.
    adongnm = models.TextField(db_column='adongNm', blank=True, null=True)  # Field name made lowercase.
    rdnmcd = models.TextField(db_column='rdnmCd', blank=True, null=True)  # Field name made lowercase.
    rdnm = models.TextField(blank=True, null=True)
    lon = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul_store_data_pre_proc'
