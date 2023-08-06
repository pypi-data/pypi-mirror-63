# import os
# import sys
# import math
# import copy
# import datetime
# import traceback
# import random
# import json
# import base64
# import zlib
# import tempfile
# import clickhouse_driver
# import numpy as np
# from redis import StrictRedis
# import _pickle as cPickle
# from lxml import etree
# import pandas as pd
# from pg_tasks_queue.Database import PgDatabase
#
#
# class DateTime:
#
#     @staticmethod
#     def np_datetime64_to_datetime(np_datetime64):
#         return datetime.datetime.utcfromtimestamp((np_datetime64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))
#
#     @staticmethod
#     def start_of_day(timestamp):
#         return datetime.datetime.strptime(timestamp.strftime('%Y-%m-%d 00:00'), '%Y-%m-%d 00:00')
#
#     @staticmethod
#     def start_of_min(timestamp):
#         return datetime.datetime.strptime(timestamp.strftime('%Y-%m-%d %H:%M:00'), '%Y-%m-%d %H:%M:00')
#
#     @staticmethod
#     def get_msec_string(time_msec):
#         return '{time_msec:,.3f}'.format(time_msec=time_msec).replace(',', '`')
#
#     @staticmethod
#     def get_sec_string(time_sec):
#         return '{time_sec:,.0f}'.format(time_sec=time_sec).replace(',', '`')
#
#     @staticmethod
#     def get_timedelta_msec(end_time, start_time):
#         return (end_time - start_time).total_seconds() * 1000
#
#     @staticmethod
#     def get_timedelta_msec_string(end_time, start_time):
#         time_msec = DateTime.get_timedelta_msec(end_time, start_time)
#         return DateTime.get_msec_string(time_msec=time_msec)
#
#     @staticmethod
#     def to_utc(timestamp=None):
#         if not timestamp:
#             return datetime.datetime.utcnow()
#         else:
#             utc_offcet_timedelta = datetime.datetime.utcnow() - datetime.datetime.now()
#             return timestamp + utc_offcet_timedelta
#
#     @staticmethod
#     def from_utc(timestamp=None):
#         if not timestamp:
#             return datetime.datetime.now()
#         else:
#             utc_offcet_timedelta = datetime.datetime.utcnow() - datetime.datetime.now()
#             return timestamp - utc_offcet_timedelta
#
#     @staticmethod
#     def get_standart_date(test_date, candle_length, up=False):
#         _date = copy.deepcopy(test_date)
#         if candle_length in [2, 3, 4, 5, 10, 15, 20, 30]:
#             rest = _date.minute % candle_length
#             if rest != 0:
#                 _date -= datetime.timedelta(minutes=int(rest))
#         if up:
#             _date += datetime.timedelta(minutes=int(candle_length))
#         return _date
#
#
# class RecommenderSystem:
#
#     @staticmethod
#     def get_dict_by_key_from_df(df, key_column=None, with_key_column=True):
#         result_dict = dict()
#         df_list = df.to_dict(orient='records')
#         counter = 0
#         for row in df_list:
#             key = counter if key_column is None else row.get(key_column)
#             if key_column is not None and not with_key_column:
#                 del row[key_column]
#             result_dict[key] = row
#             counter += 1
#         return result_dict
#
#     @classmethod
#     def get_columns_form_dict(cls, _dict):
#         err_str = f'Error in Helper.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         if len(_dict) == 0:
#             return f'{err_str}: len(_dict) == 0'
#         first_row_dict = list(_dict.values())[0]
#         if not isinstance(first_row_dict, dict):
#             return f'{err_str}: not isinstance(first_row_dict, dict)'
#         return list(first_row_dict.keys())
#
#     @classmethod
#     def get_df_from_dict(cls, _dict, key_column='id'):
#         err_str = f'Error in Helper.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         result_columns = RecommenderSystem.get_columns_form_dict(_dict)
#         if isinstance(result_columns, str):
#             return f'{err_str}: {result_columns}'
#         result_df = pd.DataFrame(list(_dict.values()), columns=result_columns)
#         if key_column is not None:
#             result_df[key_column] = list(_dict.keys())
#             result_columns.insert(0, key_column)
#             result_df = result_df.reindex(columns=result_columns)
#         result_df.reset_index(drop=True, inplace=True)
#         return result_df
#
#     @classmethod
#     def upload_from_xml(cls, upload_filename, only_date=False):
#
#         func_name = f'Helper.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#
#         try:
#             if not os.path.exists(upload_filename):
#                 return f'Error in {func_name}: upload_filename "{upload_filename}" not exists...'
#
#             with open(upload_filename, 'rb') as f:
#                 root = etree.fromstring(f.read())
#                 f.close()
#                 if root.tag != 'yml_catalog':
#                     return f"Error in {func_name}: root.tag != 'yml_catalog'..."
#
#                 load_date_str = root.get('date')
#                 if load_date_str is None:
#                     return f"Error in {func_name}: root.get('date') is None..."
#
#                 if only_date:
#                     return {'upload_date': load_date_str}
#
#                 if len(root.getchildren()) != 1:
#                     return f"Error in {func_name}: len(root.getchildren()) != 1..."
#
#                 shop = root.getchildren()[0]
#                 if shop.tag != 'shop':
#                     return f"Error in {func_name}: shop.tag != 'shop'..."
#
#                 categories_dict = dict()
#                 products_dict = dict()
#                 keys_list = list()
#                 for shop_children in shop.getchildren():
#                     if shop_children.tag == 'categories':
#                         for category in shop_children.getchildren():
#                             categories_dict[category.get('id')] = {'name': category.text,
#                                                                    'parent_id': category.get('parentId'),
#                                                                    'childs': list(),
#                                                                    'products': list(),
#                                                                    'parents': list()}
#                     elif shop_children.tag == 'offers':
#                         for offer in shop_children.getchildren():
#                             product_dict = {'available': True if offer.get('available') else False}
#                             for offer_children in offer.getchildren():
#                                 key = offer_children.tag
#                                 value = offer_children.text
#                                 if key == 'categoryId':
#                                     key = 'category_id'
#                                 elif key == 'created':
#                                     value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
#                                 elif key == 'discount_end':
#                                     value = datetime.datetime.strptime(value, '%Y-%m-%d')
#                                 elif key in ['price', 'discount', 'min_price_30']:
#                                     value = float(value)
#                                 if key not in keys_list:
#                                     keys_list.append(key)
#                                 product_dict[key] = value
#                             products_dict[offer.get('id')] = product_dict
#                     else:
#                         return f"Error in {func_name}: unknown shop_children.tag: '{shop_children.tag}'..."
#
#                 return {'categories_dict': categories_dict, 'products_dict': products_dict,
#                         'keys_list': keys_list, 'upload_date': load_date_str}
#
#         except Exception as e:
#             return f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
#
#     @staticmethod
#     def cat_and_sort_rs_burning_discounts(burning_discounts_df):
#         burning_discounts_df = copy.deepcopy(burning_discounts_df)
#         burning_discounts_df.sort_values(['discount_end', 'discount'], ascending=[True, False], inplace=True)
#         start_of_day = DateTime.start_of_day(datetime.datetime.now())
#         burning_discounts_df = burning_discounts_df.loc[burning_discounts_df.discount_end >= start_of_day]
#         burning_discounts_df = burning_discounts_df.loc[burning_discounts_df.discount > .0]
#         burning_discounts_df.reset_index(drop=True, inplace=True)
#         return burning_discounts_df
#
#     @classmethod
#     def get_rs_burning_discounts(cls, products_dict):
#         err_str = f'Error in Helper.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         burning_discounts_df = RecommenderSystem.get_df_from_dict(products_dict)
#         if isinstance(burning_discounts_df, str):
#             print(f'{err_str}: {burning_discounts_df}')
#             return None
#         for column in burning_discounts_df.columns.values:
#             if column not in ['id', 'discount', 'discount_end']:
#                 del burning_discounts_df[column]
#         return RecommenderSystem.cat_and_sort_rs_burning_discounts(burning_discounts_df)
#
#     @classmethod
#     def get_rs_burning_products(cls, products_dict):
#         err_str = f'Error in Helper.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         result_df = RecommenderSystem.get_df_from_dict(products_dict)
#         if isinstance(result_df, str):
#             print(f'{err_str}: {result_df}')
#             return None
#         for column in result_df.columns.values:
#             if column not in ['id', 'price', 'min_price_30']:
#                 del result_df[column]
#         result_df = result_df.loc[result_df.price > .0]
#         result_df = result_df.loc[result_df.min_price_30 > .0]
#         result_df['delta'] = result_df['min_price_30']/result_df['price'] - 1
#         result_df = result_df.loc[result_df.delta > .0]
#         result_df.sort_values(['delta'], ascending=[False], inplace=True)
#         result_df.reset_index(drop=True, inplace=True)
#         return result_df
#
#     @classmethod
#     def get_rs_products_and_categories(cls, categories_dict, products_dict):
#         err_str = f'Error in Helper.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#
#         try:
#             categories = copy.deepcopy(categories_dict)
#
#             first_level = list()
#
#             for category_id, category_dict in categories.items():
#
#                 def update_category_keys(_dict):
#                     keys = list(_dict.keys())
#                     for key in keys:
#                         if key not in ['parent_id', 'childs', 'products', 'parents']:
#                             del _dict[key]
#                     if _dict.get('childs') is None:
#                         _dict['childs'] = list()
#                     if _dict.get('products') is None:
#                         _dict['products'] = list()
#                     if _dict.get('parents') is None:
#                         _dict['parents'] = list()
#
#                 update_category_keys(category_dict)
#
#                 parent_id = category_dict.get('parent_id')
#                 if parent_id is None:
#                     if category_id not in first_level:
#                         first_level.append(category_id)
#                 else:
#                     parent_dict = categories.get(parent_id)
#                     if parent_dict is None:
#                         print(f'{err_str}: not found parent_dict for parent_id = {parent_id}')
#                         return None
#                     update_category_keys(parent_dict)
#                     if category_id not in parent_dict.get('childs'):
#                         parent_dict.get('childs').append(category_id)
#
#                     parents_list = list()
#                     parents_list.append(parent_id)
#                     while parent_id is not None:
#                         if parent_id not in parents_list:
#                             parents_list.append(parent_id)
#                         parent_dict = categories.get(parent_id)
#                         if parent_dict is None:
#                             print(f'{err_str}: not found parent_dict for parent_id = {parent_id}')
#                             return None
#                         parent_id = parent_dict.get('parent_id')
#                     category_dict['parents'] = parents_list
#                 categories[category_id] = category_dict
#
#             products = copy.deepcopy(products_dict)
#
#             last_level = list()
#             for product_id, product_dict in products.items():
#
#                 def update_product_keys(_dict):
#                     keys = list(_dict.keys())
#                     for key in keys:
#                         if key not in ['category_id', 'available']:
#                             del _dict[key]
#                     if _dict.get('category_id') is None:
#                         _dict['category_id'] = 'None'
#                     if _dict.get('available') is None:
#                         _dict['available'] = False
#
#                 update_product_keys(product_dict)
#
#                 category_id = product_dict.get("category_id")
#                 if category_id not in last_level:
#                     last_level.append(category_id)
#                 category_dict = categories.get(category_id)
#                 if category_dict is None:
#                     print(f'{err_str}: not found category_dict for id = {category_id}; product_id: {product_id}; '
#                                  f'product_dict: {product_dict}')
#                     return None
#                 category_dict.get('products').append(product_id)
#                 parent_id = category_dict.get('parent_id')
#                 while parent_id is not None:
#                     parent_dict = categories.get(parent_id)
#                     parent_dict.get('products').append(product_id)
#                     parent_id = parent_dict.get('parent_id')
#
#             return {'products_dict': products, 'categories_dict': categories,
#                     'first_level_list': first_level, 'last_level_list': last_level}
#         except Exception as e:
#             print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @staticmethod
#     def get_rating_df(_df, triggers_coefs_dict):
#         def get_row_rating(row):
#             trigger_type = row.get('trigger_type')
#             row_rating = triggers_coefs_dict.get(trigger_type, 0)
#             return row_rating
#         result_df = copy.deepcopy(_df)
#         result_df['rating_coef'] = result_df.apply(lambda row: get_row_rating(row), axis=1)
#         result_df['rating'] = result_df['count'] * result_df['rating_coef']
#         mask = result_df['trigger_type'].isin(list(triggers_coefs_dict.keys()))
#         result_df = result_df[mask]
#         columns = list(result_df.columns.values)
#         for column in columns:
#             if column not in ['id', 'rating']:
#                 del result_df[column]
#         result_df = result_df.groupby(['id'], as_index=False).sum()
#         result_df = result_df.loc[result_df.rating > .0]
#         result_df.sort_values(['rating'], ascending=[False], inplace=True)
#         result_df.reset_index(drop=True, inplace=True)
#         return result_df
#
# class Compress:
#
#     @staticmethod
#     def dumps(data, dump_types=['pickle', 'zlib']):
#         try:
#             dump_data = copy.deepcopy(data)
#             for dump_type in dump_types:
#                 if dump_type not in ['pickle', 'zlib', 'json']:
#                     print(f'Error in Compress.dumps(): dump_type "{dump_type}" not in [pickle, zlib, json]')
#                     return None
#                 if dump_type == 'json':
#                     dump_data = json.dumps(dump_data).encode('utf-8')
#                 elif dump_type == 'pickle':
#                     dump_data = cPickle.dumps(dump_data)
#                 elif dump_type == 'zlib':
#                     dump_data = zlib.compress(dump_data)
#             return dump_data
#         except Exception as e:
#             print(f'Error in Compress.dumps(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @staticmethod
#     def dumps_base64(data, dump_types=['pickle', 'zlib']):
#         try:
#             dump_data = Compress.dumps(data, dump_types=dump_types)
#             if dump_data is None:
#                 return None
#             return base64.b64encode(dump_data).decode("utf-8")
#         except Exception as e:
#             print(f'Error in Compress.dumps_base64(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @staticmethod
#     def loads(data, dump_types=['zlib', 'pickle']):
#         try:
#             dump_data = copy.deepcopy(data)
#             for dump_type in dump_types:
#                 if dump_type not in ['pickle', 'zlib', 'json']:
#                     print(f'Error in Compress.loads(): dump_type "{dump_type}" not in [pickle, zlib, json]')
#                     return None
#                 if dump_type == 'json':
#                     dump_data = json.loads(dump_data.decode('utf-8'))
#                 elif dump_type == 'pickle':
#                     dump_data = cPickle.loads(dump_data)
#                 elif dump_type == 'zlib':
#                     dump_data = zlib.decompress(dump_data)
#             return dump_data
#         except Exception as e:
#             print(f'Error in Compress.loads(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @staticmethod
#     def loads_base64(data, dump_types=['zlib', 'pickle']):
#         try:
#             if data is None:
#                 return None
#             dump_data = base64.b64decode(copy.deepcopy(data))
#             return Compress.loads(dump_data, dump_types=dump_types)
#         except Exception as e:
#             print(f'Error in Compress.loads_base64(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @staticmethod
#     def dump(data, filename, dump_types=['pickle', 'zlib']):
#         try:
#             dump_data = Compress.dumps(data, dump_types=dump_types)
#             if dump_data is None:
#                 return False
#             with open(filename, 'wb') as f:
#                 f.write(dump_data)
#                 f.close()
#             return True
#         except Exception as e:
#             print(f'Error in Compress.dump(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return False
#
#     @staticmethod
#     def load(filename, dump_types=['zlib', 'pickle']):
#         try:
#             with open(filename, 'rb') as f:
#                 data = f.read()
#                 f.close()
#                 return Compress.loads(data, dump_types=dump_types)
#         except Exception as e:
#             print(f'Error in Compress.dump(): {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#
# class ClickHouse:
#
#     _settings = None
#     _client = None
#
#     def __init__(self, settings=None):
#         self._settings = settings
#
#     def get_attr(self, attr_name):
#         return self._settings.get(attr_name)
#
#     def connect(self, close_connection=False):
#         err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
#         try:
#             if not isinstance(self._settings, dict):
#                 print(f'{err_str}: not isinstance(self._settingsm dict)')
#                 self.disconnect()
#                 return False
#
#             client_dict = dict()
#             for k, v in copy.deepcopy(self._settings).items():
#                 if k in ['host', 'port', 'database', 'user', 'password', 'secure', 'verify', 'compression']:
#                     if k in ['secure', 'verify', 'compression']:
#                         v = True if v.lower().strip == 'true' else False
#                     client_dict[k] = v
#
#             if client_dict.get('host') is None:
#                 client_dict['host'] = 'localhost'
#
#             if client_dict.get('password') and client_dict.get('password').lower() == '<none>':
#                 del client_dict['password']
#
#             self._client = clickhouse_driver.Client(**client_dict)
#             try:
#                 self._client.execute('select version()')
#             except Exception as e:
#                 print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#                 self._client = None
#                 return False
#
#             if close_connection:
#                 self.disconnect()
#             return True
#         except Exception as e:
#             print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             self._client = None
#             return False
#
#     def disconnect(self):
#         err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
#         if self._client is not None:
#             try:
#                 self._client.disconnect()
#             except Exception as e:
#                 print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             finally:
#                 self._client = None
#
#     def _connect_to_db(self):
#         self._result = None
#         if self._client is not None:
#             return True
#         self.connect()
#         return False if self._client is None else True
#
#     def execute_sql_string(self, sql_string, params=None, with_column_types=True):
#         err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
#         close_connection = True if self._client is None else False
#         if not self._connect_to_db():
#             return None
#         try:
#             res = self._client.execute(sql_string, params, with_column_types)
#             return res
#         except Exception as e:
#             print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#         finally:
#             if close_connection:
#                 self.disconnect()
#
#     def insert_values_list(self, sql_string, values_list):
#         err_str = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
#         close_connection = True if self._client is None else False
#         if not self._connect_to_db():
#             return None
#         try:
#             res = self._client.execute(sql_string, values_list)
#             return res
#         except Exception as e:
#             print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#         finally:
#             if close_connection:
#                 self.disconnect()
#
#
# class EcroDatabase:
#     pg_database = None
#
#     @classmethod
#     def init(cls, database_dict):
#         err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
#         pg_database = PgDatabase(database_dict)
#         if pg_database.connect(close_connection=True):
#             print(f'Success connect to database "{database_dict.get("dbname")}"')
#             EcroDatabase.pg_database = pg_database
#             return True
#         print(f'{err_str}: database "{database_dict.get("dbname")}" not available')
#         return False
#
#     @classmethod
#     def get_products(cls):
#         err_str = f'Error in RsDatabase.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         if EcroDatabase.pg_database is None:
#             print(f'{err_str}: EcroDatabase.pg_database is None...')
#             return None
#         schema = EcroDatabase.pg_database.get_attr('schema')
#         sql_string = """
#             select
#                 --count(*) OVER() as cnt,
#                 products."Id" as id,
#                 products."Status" as status,
#                 products."Title" as title,
#                 products."Description" as description,
#                 products."Brand" as brand,
#                 products."Price" as price,
#                 products."SalePrice" as sale_price,
#                 products."DiscountPercent" as discount_percent,
#                 products."UnitsAvailable" as units_available,
#                 products."WhenCreated" as created,
#                 products."LotCategoryId" as category_id
#             from
#                 {schema}."Lots" as products
#         """.format(
#             schema=schema
#         )
#
#         result = EcroDatabase.pg_database.select(sql_string)
#         if not isinstance(result, list):
#             print(f'{err_str}: sql.result(0) is not list')
#             return None
#         if len(result) == 0:
#             print(f'{err_str}: len(sql.result(0)) = 0')
#             return None
#         df = pd.DataFrame.from_dict(result)
#         created_2000 = datetime.datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
#         df['created'] = df['created'].apply(lambda x: created_2000 if x is None else x)
#         df['created'] = df['created'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
#
#         df['sale_price'] = df['sale_price'].apply(lambda x: .0 if x is None else x)
#         df['discount_percent'] = df['discount_percent'].apply(lambda x: .0 if x is None else x)
#
#         return df
#
#     @classmethod
#     def get_categories(cls):
#         err_str = f'Error in RsDatabase.{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         if EcroDatabase.pg_database is None:
#             print(f'{err_str}: EcroDatabase.pg_database is None...')
#             return None
#         schema = EcroDatabase.pg_database.get_attr('schema')
#
#         sql_string = """
#             select
#                 "Id" as id,
#                 "Name" as "name",
#                 "ParentLotCategoryId" as parent_id
#             from
#                 {schema}."LotCategories"
#         """.format(
#             schema=schema
#         )
#         result = EcroDatabase.pg_database.select(sql_string)
#         if not isinstance(result, list):
#             print(f'{err_str}: sql.result(0) is not list')
#             return None
#         if len(result) == 0:
#             print(f'{err_str}: len(sql.result(0)) = 0')
#             return None
#         df = pd.DataFrame.from_dict(result)
#         return df
#
#
# class Redis:
#
#     Redis = None
#     ecro_uuid = '270aea41-c809-409a-baf4-215c2245d76e'
#
#     @classmethod
#     def init(cls, redis_cfg):
#         err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
#         if not isinstance(redis_cfg, dict):
#             print(f'{err_str}: not isinstance(redis_cfg, dict)...')
#             return False
#
#         redis_config = dict(host=redis_cfg.get('host', '127.0.0.1'),
#                             port=int(redis_cfg.get('port', '6379')),
#                             db=int(redis_cfg.get('db', 0)))
#         if redis_cfg.get('password') is not None:
#             redis_config['password'] = redis_cfg.get('password')
#
#         Redis = StrictRedis(**redis_config)
#         try:
#             Redis.ping()
#             Redis.Redis = Redis
#         except Exception as e:
#             print(f'{err_str}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return False
#
#         return True
#
#     @classmethod
#     def get_redis_value(cls, _key):
#         func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         try:
#             if Redis.Redis is None:
#                 print(f'Error in {func_name}: Redis is None...')
#                 return None
#             if _key is None:
#                 print(f'Error in {func_name}: _key is None...')
#                 return None
#             Redis_value = Redis.Redis.get(_key)
#             return Compress.loads_base64(Redis_value)
#         except Exception as e:
#             print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @classmethod
#     def get_redis_keys(cls, pattern):
#         func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         try:
#             if Redis.Redis is None:
#                 print(f'Error in {func_name}: Redis is None...')
#                 return None
#             if pattern is None:
#                 print(f'Error in {func_name}: pattern is None...')
#                 return None
#             return Redis.Redis.keys(pattern=pattern)
#         except Exception as e:
#             print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return None
#
#     @classmethod
#     def delete_redis_keys(cls, *keys):
#         func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         try:
#             if Redis.Redis is None:
#                 print(f'Error in {func_name}: Redis is None...')
#                 return False
#             if keys is None:
#                 print(f'Error in {func_name}: keys is None...')
#                 return False
#             res = Redis.Redis.delete(*keys)
#             return True
#         except Exception as e:
#             print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return False
#
#     @classmethod
#     def update_redis_value(cls, _key, _value, force=False):
#         func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
#         try:
#             if _key is None:
#                 print(f'Error in {func_name}: _key is None...')
#                 return False
#             if _value is None:
#                 print(f'Error in {func_name}: _value is None...')
#                 return False
#             if Redis.Redis is None:
#                 print(f'Error in {func_name}: Redis is None...')
#                 return False
#             if not force:
#                 Redis_value = Redis.Redis.get(_key)
#                 if Redis_value is None:
#                     force = True
#             if force:
#                 write_value = Compress.dumps_base64(copy.deepcopy(_value))
#                 return Redis.Redis.set(_key, write_value)
#             return True
#         except Exception as e:
#             print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return False
#
#     @classmethod
#     def update_redis_values_from_xml_file(cls, xml_filename, ChDatabase, uuid=None, force=False):
#         func_name = f'{cls.__name__}.{sys._getframe().f_code.co_name}()'
#
#         def get_xml_dict(upload_filename, only_date=False):
#             xmlfile_dict = RecommenderSystem.upload_from_xml(upload_filename, only_date=only_date)
#             if isinstance(xmlfile_dict, str):
#                 print(f'Error in {func_name}: {xmlfile_dict}')
#                 return None
#             if not isinstance(xmlfile_dict, dict):
#                 print(f'Error in {func_name}: helper.RecommenderSystem.upload_from_xml() not dict...')
#                 return None
#             return xmlfile_dict
#
#         try:
#             if Redis.Redis is None:
#                 print(f'Error in {func_name}: self.Redis is None...')
#                 return False
#             if uuid is None:
#                 uuid = Redis.ecro_uuid
#
#             partner_id = f'recommender_system:{uuid}'
#
#             if not os.path.exists(xml_filename):
#                 print(f'Error in {func_name}: xml_filename "{xml_filename}" not exists...')
#                 return False
#
#             if not force and Redis.get_redis_value(f'{partner_id}:upload_date') is None:
#                 force = True
#             if not force and Redis.get_redis_value(f'{partner_id}:categories_dict') is None:
#                 force = True
#             if not force and Redis.get_redis_value(f'{partner_id}:products_dict') is None:
#                 force = True
#             if not force and Redis.get_redis_value(f'{partner_id}:upload_date') is not None:
#                 xmlfile_dict = get_xml_dict(xml_filename, only_date=True)
#                 if xmlfile_dict is None:
#                     return False
#                 if xmlfile_dict.get('upload_date') != Redis.get_redis_value(f'{partner_id}:upload_date'):
#                     print(f'{func_name}: get new upload file; upload_date: "{xmlfile_dict.get("upload_date")}"')
#                     force = True
#
#             if force:
#                 partner_pattern = f'{partner_id}:*'
#                 partner_keys = Redis.get_redis_keys(partner_pattern)
#                 if not isinstance(partner_keys, list):
#                     print(f'Error in {func_name}: not isinstance({partner_keys}, list)...')
#                     return False
#                 if len(partner_keys) > 0:
#                     if not Redis.delete_redis_keys(*partner_keys):
#                         print(f'Error in {func_name}: not self.delete_redis_keys(*partner_keys)...')
#                 partner_keys = Redis.get_redis_keys(partner_pattern)
#                 if not isinstance(partner_keys, list):
#                     print(f'Error in {func_name}: not isinstance(partner_keys, list)...')
#                     return False
#                 if not len(partner_keys) == 0:
#                     print(f'Error in {func_name}: not len(partner_keys) == 0...')
#                     return False
#
#                 xmlfile_dict = get_xml_dict(xml_filename)
#                 if xmlfile_dict is None:
#                     return False
#
#                 if not Redis.update_redis_value(f'{partner_id}:categories_dict', xmlfile_dict.get('categories_dict'),
#                                                 force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(categories_dict)...')
#                     return False
#
#                 if not Redis.update_redis_value(f'{partner_id}:products_dict', xmlfile_dict.get('products_dict'),
#                                                 force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(products_dict)...')
#                     return False
#
#                 if not Redis.update_redis_value(f'{partner_id}:upload_date', xmlfile_dict.get('upload_date'),
#                                                 force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(upload_date)...')
#                     return False
#
#             if force or (Redis.get_redis_value(f'{partner_id}:rs_burning_discounts') is None
#                          or Redis.get_redis_value(f'{partner_id}:rs_burning_products') is None):
#
#                 products_dict = Redis.get_redis_value(f'{partner_id}:products_dict')
#                 if products_dict is None:
#                     print(f'Error in {func_name}: get_redis_value(products_dict) is None...')
#                     return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_burning_discounts') is None:
#                     rs_burning_discounts = RecommenderSystem.get_rs_burning_discounts(products_dict)
#                     if rs_burning_discounts is None:
#                         print(f'Error in {func_name}: get_rs_burning_discounts(products_dict) is None...')
#                         return False
#                     if not Redis.update_redis_value(f'{partner_id}:rs_burning_discounts', rs_burning_discounts,
#                                                     force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_burning_discounts)...')
#                         return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_burning_products') is None:
#                     rs_burning_products = RecommenderSystem.get_rs_burning_products(products_dict)
#                     if rs_burning_products is None:
#                         print(f'Error in {func_name}: rs_burning_products(products_dict) is None...')
#                         return False
#                     if not Redis.update_redis_value(f'{partner_id}:rs_burning_products', rs_burning_products,
#                                                     force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_burning_products)...')
#                         return False
#
#             if force or (Redis.get_redis_value(f'{partner_id}:rs_products_dict') is None
#                          or Redis.get_redis_value(f'{partner_id}:rs_categories_dict') is None
#                          or Redis.get_redis_value(f'{partner_id}:rs_first_level_list') is None
#                          or Redis.get_redis_value(f'{partner_id}:rs_last_level_list') is None):
#
#                 categories_dict = Redis.get_redis_value(f'{partner_id}:categories_dict')
#                 if categories_dict is None:
#                     print(f'Error in {func_name}: get_redis_value(categories_dict) is None...')
#                     return False
#                 products_dict = Redis.get_redis_value(f'{partner_id}:products_dict')
#                 if products_dict is None:
#                     print(f'Error in {func_name}: get_redis_value(products_dict) is None...')
#                     return False
#
#                 rs_products_and_categories = RecommenderSystem.get_rs_products_and_categories(categories_dict,
#                                                                                               products_dict)
#                 if rs_products_and_categories is None:
#                     print(f'Error in {func_name}: rs_products_and_categories is None...')
#                     return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_products_dict') is None:
#                     if not Redis.update_redis_value(f'{partner_id}:rs_products_dict',
#                                                     rs_products_and_categories.get('products_dict'), force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_products_dict)...')
#                         return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_categories_dict') is None:
#                     if not Redis.update_redis_value(f'{partner_id}:rs_categories_dict',
#                                                     rs_products_and_categories.get('categories_dict'), force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_categories_dict)...')
#                         return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_first_level_list') is None:
#                     if not Redis.update_redis_value(f'{partner_id}:rs_first_level_list',
#                                                     rs_products_and_categories.get('first_level_list'), force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_first_level_list)...')
#                         return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_last_level_list') is None:
#                     if not Redis.update_redis_value(f'{partner_id}:rs_last_level_list',
#                                                     rs_products_and_categories.get('last_level_list'), force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_flast_level_list)...')
#                         return False
#
#             if force or Redis.get_redis_value(f'{partner_id}:rs_sales_df') is None:
#                 rs_sales_df = ChDatabase.get_triggers_count(partner_id=uuid)
#                 if not Redis.update_redis_value(f'{partner_id}:rs_sales_df', rs_sales_df, force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(rs_sales_df)...')
#                     return False
#
#             if force or Redis.get_redis_value(f'{partner_id}:rs_product_views_df') is None:
#                 rs_product_views_df = ChDatabase.get_triggers_count(partner_id=uuid, trigger_type=2)
#                 if not Redis.update_redis_value(f'{partner_id}:rs_product_views_df', rs_product_views_df, force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(rs_product_views_df)...')
#                     return False
#
#             if force or Redis.get_redis_value(f'{partner_id}:rs_rating_df') is None:
#                 rs_rating_df = ChDatabase.get_triggers_counts(partner_id=uuid)
#                 if rs_rating_df is None:
#                     print(f'Error in {func_name}: ChDatabase.get_triggers_counts() is None...')
#                     return False
#                 triggers_coefs_dict = {2: 1., 5: 10.}
#                 rs_rating_df = RecommenderSystem.get_rating_df(rs_rating_df, triggers_coefs_dict)
#                 if not Redis.update_redis_value(f'{partner_id}:rs_rating_df', rs_rating_df, force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(rs_rating_df)...')
#                     return False
#
#             rs_category_views_df = Redis.get_redis_value(f'{partner_id}:rs_category_views_df')
#             if force or rs_category_views_df is None:
#                 rs_category_views_df = ChDatabase.get_triggers_count(partner_id=uuid, trigger_type=1)
#                 if not Redis.update_redis_value(f'{partner_id}:rs_category_views_df', rs_category_views_df, force=force):
#                     print(f'Error in {func_name}: error in update_redis_value(rs_category_views_df)...')
#                     return False
#
#             if force or (Redis.get_redis_value(f'{partner_id}:rs_last_category_views_df') is None
#                          or Redis.get_redis_value(f'{partner_id}:rs_first_category_views_df') is None):
#
#                 rs_category_views_df = Redis.get_redis_value(f'{partner_id}:rs_category_views_df')
#                 if rs_category_views_df is None:
#                     print(f'Error in {func_name}: get_redis_value(rs_category_views_df) is None ...')
#                     return False
#                 rs_category_views_df.sort_values(by=['count'], ascending=[0], inplace=True)
#                 rs_category_views_df = rs_category_views_df.reset_index(drop=True)
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_last_category_views_df') is None:
#                     rs_last_level_list = Redis.get_redis_value(f'{partner_id}:rs_last_level_list')
#                     if rs_last_level_list is None:
#                         print(f'Error in {func_name}: get_redis_value(rs_last_level_list) is None ...')
#                         return False
#
#                     rs_last_category_views_df = copy.deepcopy(rs_category_views_df)
#                     mask = rs_last_category_views_df['id'].isin(rs_last_level_list)
#                     rs_last_category_views_df = rs_last_category_views_df[mask]
#
#                     rs_last_category_views_df.sort_values(by=['count'], ascending=[0], inplace=True)
#                     rs_last_category_views_df = rs_last_category_views_df.reset_index(drop=True)
#
#                     if not Redis.update_redis_value(f'{partner_id}:rs_last_category_views_df',
#                                                     rs_last_category_views_df, force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_last_category_views_df)...')
#                         return False
#
#                 if force or Redis.get_redis_value(f'{partner_id}:rs_first_category_views_df') is None:
#                     rs_first_level_list = Redis.get_redis_value(f'{partner_id}:rs_first_level_list')
#                     if rs_first_level_list is None:
#                         print(f'Error in {func_name}: get_redis_value(rs_first_level_list) is None ...')
#                         return False
#
#                     rs_first_category_views_df = copy.deepcopy(rs_category_views_df)
#                     mask = rs_first_category_views_df['id'].isin(rs_first_level_list)
#                     rs_first_category_views_df = rs_first_category_views_df[mask]
#
#                     rs_first_category_views_df.sort_values(by=['count'], ascending=[0], inplace=True)
#                     rs_first_category_views_df = rs_first_category_views_df.reset_index(drop=True)
#
#                     if not Redis.update_redis_value(f'{partner_id}:rs_first_category_views_df',
#                                                     rs_first_category_views_df, force=force):
#                         print(f'Error in {func_name}: error in update_redis_value(rs_first_category_views_df)...')
#                         return False
#
#             return True
#
#         except Exception as e:
#             print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
#             return False
#
#
# class ChDatabase:
#     ChDatabase = None
#
#     @classmethod
#     def init(cls, database_dict):
#         err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
#         ChDatabase = ClickHouse(database_dict)
#         if not ChDatabase.connect(close_connection=True):
#             print(f'{err_str}: not ChDatabase.connect()')
#             return False
#         ChDatabase.ChDatabase = ChDatabase
#         return True
#
#     @staticmethod
#     def get_clickhouse_columns(result_1):
#         columns = list()
#         for column in result_1:
#             columns.append(column[0])
#         return columns
#
#     @classmethod
#     def get_triggers_count(cls, partner_id, trigger_type=5):
#         err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
#         if partner_id is None:
#             print(f'{err_str}: partner_id is None')
#             return None
#         if ChDatabase.ChDatabase is None:
#             print(f'{err_str}: ClickHouse.ChDatabase is None')
#             return None
#         dbname = ChDatabase.ChDatabase.get_attr('dbname')
#         sql_string = """
#             SELECT
#                 item_id as "id",
#                 COUNT(item_id) as "count"
#             FROM
#                 {dbname}."triggers"
#             WHERE trigger_type={trigger_type} AND partner_id='{partner_id}'
#             GROUP BY item_id
#             ORDER BY COUNT(item_id) DESC
#         """.format(
#             dbname=dbname,
#             trigger_type=trigger_type,
#             partner_id=partner_id
#         )
#         result = ChDatabase.ChDatabase.execute_sql_string(sql_string)
#         if not isinstance(result, tuple):
#             print(f'{err_str}: result is tuple')
#             return None
#         df = pd.DataFrame(result[0], columns=ChDatabase.get_clickhouse_columns(result[1]))
#         df = df.reset_index(drop=True)
#         return df
#
#     @classmethod
#     def get_triggers_counts(cls, partner_id):
#         err_str = f'Error in {cls.__name__}.{sys._getframe().f_code.co_name}()'
#         if partner_id is None:
#             print(f'{err_str}: partner_id is None')
#             return None
#         if ChDatabase.ChDatabase is None:
#             print(f'{err_str}: ClickHouse.ChDatabase is None')
#             return None
#         dbname = ChDatabase.ChDatabase.get_attr('dbname')
#         sql_string = """
#             SELECT
#                 item_id as "id",
#                 trigger_type,
#                 COUNT(item_id) as "count"
#             FROM
#                 {dbname}."triggers"
#             WHERE partner_id='{partner_id}'
#             GROUP BY item_id, trigger_type
#             ORDER BY item_id ASC, trigger_type DESC
#         """.format(
#             dbname=dbname,
#             partner_id=partner_id
#         )
#         result = ChDatabase.ChDatabase.execute_sql_string(sql_string)
#         if not isinstance(result, tuple):
#             print(f'{err_str}: result is tuple')
#             return None
#         df = pd.DataFrame(result[0], columns=ChDatabase.get_clickhouse_columns(result[1]))
#         df = df.reset_index(drop=True)
#         return df
#
#
# def get_ecro_products_and_categories(EcroDatabase_cfg):
#     func_name = f'{sys._getframe().f_code.co_name}()'
#     try:
#         if not isinstance(EcroDatabase_cfg, dict):
#             return f'Error in {func_name}: not isinstance(EcroDatabase_cfg, dict)...'
#
#         if not EcroDatabase.init(EcroDatabase_cfg):
#             return f'Error in {func_name}: not EcroDatabase.init(EcroDatabase_cfg)...'
#
#         ecro_products = EcroDatabase.get_products()
#         if ecro_products is None:
#             return f'Error in {func_name}: ecro_products is None...'
#         # helper.Print.print_df(ecro_products, 'ecro_products')
#
#         ecro_categories = EcroDatabase.get_categories()
#         if ecro_categories is None:
#             return f'Error in {func_name}: ecro_categories is None...'
#         # helper.Print.print_df(ecro_categories, 'ecro_categories')
#
#         ecro_categories_dict = RecommenderSystem.get_dict_by_key_from_df(ecro_categories, 'id')
#         ecro_products_dict = RecommenderSystem.get_dict_by_key_from_df(ecro_products, 'id')
#
#         def get_parent_id(_id):
#             return None if math.isnan(_id) else int(_id)
#
#         categories_dict = dict()
#
#         for products_dict in ecro_products_dict.values():
#             # print(f'products_dict: {products_dict}')
#             category_id = products_dict.get("category_id")
#             if categories_dict.get(category_id) is None:
#                 ecro_category_dict = ecro_categories_dict.get(category_id)
#                 if ecro_category_dict is None:
#                     return f'Error in {func_name}: ecro_category_dict (id={category_id}) is None...'
#                 parent_id = get_parent_id(ecro_category_dict.get('parent_id'))
#                 category_dict = {'id': category_id, 'name': ecro_category_dict.get('name'), 'parent_id': parent_id}
#                 categories_dict[category_id] = category_dict
#                 while parent_id is not None:
#                     parent_ecro_category_dict = ecro_categories_dict.get(parent_id)
#                     if parent_ecro_category_dict is None:
#                         return f'Error in {func_name}: parent_ecro_category_dict (id={parent_id}) is None...'
#                     parent_parent_id = get_parent_id(parent_ecro_category_dict.get('parent_id'))
#                     parent_categories_dict = categories_dict.get(parent_id)
#                     if parent_categories_dict is None:
#                         parent_category = {'id': parent_id, 'name': parent_ecro_category_dict.get('name'),
#                                            'parent_id': parent_parent_id}
#                         categories_dict[parent_id] = parent_category
#                     parent_id = parent_parent_id
#
#         # print(f'len(categories_dict): {len(categories_dict)}; '
#         #       f'categories_dict: {helper.Json.json_dumps(categories_dict)}')
#
#         return {'categories_dict': categories_dict, 'products_dict': ecro_products_dict}
#
#     except Exception as e:
#         return f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
#
#
# def db_to_xml(params):
#     func_name = f'{sys._getframe().f_code.co_name}()'
#     try:
#         # print(f'{func_name}; type(params) = {type(params)}; params = {params}')
#         if not isinstance(params, dict):
#             error = f'Error in {func_name}: not isinstance(params, dict)...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         xml_filename = params.get('xml_filename')
#         if xml_filename is None:
#             error = f'Error in {func_name}: xml_filename is None...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         ecro_products_and_categories = get_ecro_products_and_categories(params.get('EcroDatabase_cfg'))
#         if isinstance(ecro_products_and_categories, str):
#             return {'status': 'error', 'result': ecro_products_and_categories}
#
#         if not isinstance(ecro_products_and_categories, dict):
#             error = f'Error in {func_name}: not isinstance(ecro_products_and_categories, dict)...'
#             print(error)
#             return {'status': 'error', 'result': error}
#         categories_dict = ecro_products_and_categories.get('categories_dict')
#         products_dict = ecro_products_and_categories.get('products_dict')
#
#         now_timestamp = datetime.datetime.now()
#         start_of_day = datetime.datetime.strptime(now_timestamp.strftime('%Y-%m-%d 00:00'), '%Y-%m-%d 00:00')
#
#         root_tag = etree.Element('yml_catalog', date=now_timestamp.strftime('%Y-%m-%d %H:%M'))
#         shop_tag = etree.SubElement(root_tag, 'shop')
#
#         categories_tag = etree.SubElement(shop_tag, 'categories')
#         for category_dict in categories_dict.values():
#             if category_dict.get('parent_id') is None:
#                 category_tag = etree.SubElement(categories_tag, 'category', id=str(category_dict.get('id')))
#             else:
#                 category_tag = etree.SubElement(categories_tag, 'category', id=str(category_dict.get('id')),
#                                                 parentId=str(category_dict.get('parent_id')))
#             category_tag.text = category_dict.get('name')
#
#         offers_tag = etree.SubElement(shop_tag, 'offers')
#         for products_dict in products_dict.values():
#             offer_tag = etree.SubElement(offers_tag, 'offer', id=str(products_dict.get('id')), available='true')
#
#             offer_name_tag = etree.SubElement(offer_tag, 'name')
#             offer_name_tag.text = products_dict.get('title')
#             # offer_url_tag = etree.SubElement(offer_tag, 'url')
#             # offer_url_tag.text = f"http://78.29.15.196:4200/product/{products_dict.get('id')}"
#             # offer_picture_tag = etree.SubElement(offer_tag, 'picture')
#             # offer_picture_tag.text = f"http://78.29.15.196:4200/images/{products_dict.get('id')}.jpg"
#
#             price = products_dict.get('price', .0)
#             offer_price_tag = etree.SubElement(offer_tag, 'price')
#             offer_price_tag.text = str(price)
#
#             offer_discount_tag = etree.SubElement(offer_tag, 'discount')
#             offer_discount_tag.text = str(products_dict.get('discount_percent', .0))
#
#             days = random.randint(0, 100) * (1 if random.randint(0, 1) == 1 else -1)
#             discount_end = start_of_day + datetime.timedelta(days=days)
#             offer_discount_end_tag = etree.SubElement(offer_tag, 'discount_end')
#             offer_discount_end_tag.text = discount_end.strftime('%Y-%m-%d')
#
#             offer_created_tag = etree.SubElement(offer_tag, 'created')
#             offer_created_tag.text = str(products_dict.get('created', '2000-01-01 00:00:00'))
#
#             delta = random.uniform(0.0, 0.5) * (1 if random.randint(0, 1) == 1 else -1)
#             price_with_delta = price * (1 + delta)
#             offer_min_price_30_tag = etree.SubElement(offer_tag, 'min_price_30')
#             min_price_30 = round(price_with_delta, 2)
#             offer_min_price_30_tag.text = str(min_price_30)
#
#             offer_category_id_tag = etree.SubElement(offer_tag, 'categoryId')
#             offer_category_id_tag.text = str(products_dict.get('category_id'))
#
#             # description = products_dict.get('description', '').strip()
#             # offer_description_tag = etree.SubElement(offer_tag, 'description')
#             # offer_description_tag.text = description
#
#         with open(xml_filename, 'wb') as f:
#             f.write(etree.tostring(root_tag, xml_declaration=True, encoding='UTF-8', pretty_print=True))
#             f.close()
#         # print(f'Success write to {xml_filename}')
#
#         return {'status': 'finished', 'result': f'Success write to {xml_filename}'}
#
#     except Exception as e:
#         error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
#         print(error)
#         return {'status': 'error', 'result': error}
#
#
# def xml_to_redis(params):
#     func_name = f'{sys._getframe().f_code.co_name}()'
#     try:
#         # print(f'{func_name}; type(params) = {type(params)}; params = {params}')
#         if not isinstance(params, dict):
#             error = f'Error in {func_name}: not isinstance(params, dict)...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         xml_filename = params.get('xml_filename')
#         if xml_filename is None:
#             error = f'Error in {func_name}: xml_filename is None...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         redis_cfg = params.get('redis_cfg')
#         if not isinstance(redis_cfg, dict):
#             error = f'Error in {func_name}: redis_cfg is None...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         clickhouse_cfg = params.get('clickhouse_cfg')
#         if not isinstance(clickhouse_cfg, dict):
#             error = f'Error in {func_name}: clickhouse_cfg is None...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         if not Redis.init(redis_cfg):
#             error = f'Error in {func_name}: not erco_redis.init()...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         if not ChDatabase.init(clickhouse_cfg):
#             error = f'Error in {func_name}: not ChDatabase.init()...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         if not Redis.update_redis_values_from_xml_file(xml_filename, ChDatabase):
#             error = f'Error in {func_name}: not erco_redis.update_redis_values_from_xml_file()...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         return {'status': 'finished', 'result': f'Success upload from {xml_filename}'}
#
#     except Exception as e:
#         error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
#         print(error)
#         return {'status': 'error', 'result': error}
#
#
# def db_to_redis(params):
#     func_name = f'{sys._getframe().f_code.co_name}()'
#
#     def remove_file(filename):
#         try:
#             if not os.path.exists(filename):
#                 return True
#             os.remove(filename)
#             if os.path.exists(filename):
#                 return False
#             return True
#         except Exception as e:
#             return False
#
#     def get_gettempdir_filename(filename, delete=True):
#         tempdir_filename = os.path.join(tempfile.gettempdir(), filename)
#         if delete:
#             if not remove_file(tempdir_filename):
#                 return None
#         return tempdir_filename
#     try:
#         # print(f'{func_name}; type(params) = {type(params)}; params = {params}')
#         tempdir_filename = get_gettempdir_filename('db_to_redis.xml')
#         if tempdir_filename is None:
#             error = f'Error in {func_name}: tempdir_filename is None...'
#             print(error)
#             return {'status': 'error', 'result': error}
#         params['xml_filename'] = tempdir_filename
#
#         result = db_to_xml(params)
#         if result.get('status') == 'error':
#             return result
#
#         result = xml_to_redis(params)
#         if result.get('status') == 'error':
#             return result
#
#         if not remove_file(tempdir_filename):
#             error = f'Error in {func_name}: helper.Path.remove({tempdir_filename})...'
#             print(error)
#             return {'status': 'error', 'result': error}
#
#         return {'status': 'finished', 'result': 'ok'}
#     except Exception as e:
#         error = f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}'
#         print(error)
#         return {'status': 'error', 'result': error}
