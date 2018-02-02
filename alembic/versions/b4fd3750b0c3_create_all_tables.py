"""create report table

Revision ID: b4fd3750b0c3
Revises: 
Create Date: 2018-02-02 14:45:02.673645

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b4fd3750b0c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        """
        
            CREATE TYPE report_type_enum AS ENUM (
              'DAILY', 
              'WEEKLY', 
              'MONTHLY',
              'YERLY');

            CREATE TABLE t_report_setting(
                report_setting_id serial PRIMARY KEY,
                report_type report_type_enum,
                report_setting_name VARCHAR(100),
                report_setting_description VARCHAR(255),
                report_setting_email_string VARCHAR(3000),
                is_enabled BOOLEAN,
                created_at TIMESTAMP DEFAULT now(),
                updated_at TIMESTAMP
            ) WITH oids;
            
            CREATE TABLE t_report_setting_field(
                report_setting_field_id serial PRIMARY KEY,
                report_setting_id INTEGER REFERENCES t_report_setting(report_setting_id),
                field_name VARCHAR(100),
                field_description VARCHAR(100),
                is_enabled BOOLEAN,
                created_at TIMESTAMP DEFAULT now(),
                updated_at TIMESTAMP
            ) WITH oids;
            
            CREATE TABLE t_report(
                report_id serial PRIMARY KEY,
                report_setting_id INTEGER REFERENCES t_report_setting(report_setting_id),
                to_be_sent_at TIMESTAMP,
                already_sent BOOLEAN,
                created_at TIMESTAMP DEFAULT now(),
                updated_at TIMESTAMP
            ) WITH oids;
            
            CREATE TABLE t_report_field_value(
                report_field_value_id serial PRIMARY KEY,
                report_setting_field_id INTEGER REFERENCES t_report_setting_field(report_setting_field_id),
                report_id INTEGER REFERENCES t_report(report_id),
                field_value VARCHAR(100),
                created_at TIMESTAMP DEFAULT now(),
                updated_at TIMESTAMP
            ) WITH oids;
            
        """
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        """

        DROP TABLE IF EXISTS
            t_report_field_value
        ;
        
        DROP TABLE IF EXISTS
            t_report
        ;
        
        DROP TABLE IF EXISTS
            t_report_setting_field
        ;
        
        DROP TABLE IF EXISTS
            t_report_setting
        ;
        
        DROP TYPE report_type;
        """
    )
