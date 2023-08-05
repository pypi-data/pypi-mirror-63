import datetime
import psycopg2


def start_end_from_last_call(salesforce_instance, o):
    table = o.get('table')
    updated_field = o.get('updated_field')
    if not updated_field:
        updated_field = 'lastmodifieddate'
    last_n_days = o.get('last_n_days')
    if not last_n_days:
        updated_field = 1
    query = "SELECT MAX(%s) as max_ FROM %s.%s" % (updated_field, salesforce_instance.schema_prefix, table)
    try:
        result_query = salesforce_instance.datamart.execute_query(query)
        start = result_query[0]["max_"]
        if last_n_days:
            start = start + datetime.timedelta(days=-last_n_days)
        return str(start.isoformat()) + "Z"
    except (IndexError, TypeError, psycopg2.ProgrammingError) as e:
        return None
