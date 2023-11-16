from sqltocsv import bo,bs
import os

CLASSES = {
    'Python.Bs.SQLService': bs.SQLService,
    'Python.Bo.CSVOperation': bo.CSVOperation
}

db_user = os.environ.get('POSTGRES_USER', 'DemoData')
db_password = os.environ.get('POSTGRES_PASSWORD', 'DemoData')
db_host = os.environ.get('POSTGRES_HOST', 'db')
db_port = os.environ.get('POSTGRES_PORT', '5432')
db_name = os.environ.get('POSTGRES_DB', 'DemoData')

PRODUCTIONS = [{
    "Python.Production": {
        "@Name": "Python.Production",
        "@LogGeneralTraceEvents": "false",
        "Description": "",
        "ActorPoolSize": "2",
        "Item": [
            {
                "@Name": "Python.Bs.SQLService",
                "@Category": "",
                "@ClassName": "Python.Bs.SQLService",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": {
                    "@Target": "Host",
                    "@Name": "%settings",
                    "#text": "sql=select * from formation\nconn=postgresql://"+db_user+":"+db_password+"@"+db_host+":"+db_port+"/"+db_name+"\ntarget=Python.Bo.CSVOperation"
                }
            },
            {
                "@Name": "Python.Bo.CSVOperation",
                "@Category": "",
                "@ClassName": "Python.Bo.CSVOperation",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": {
                    "@Target": "Host",
                    "@Name": "%settings",
                    "#text": "filename=/tmp/export.csv"
                }
            }
        ]
    }
}]