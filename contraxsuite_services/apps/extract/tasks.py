"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
# -*- coding: utf-8 -*-

from django.db import connection

from apps.celery import app
from apps.task.tasks import BaseTask

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2020, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.5.0/LICENSE"
__version__ = "1.5.0"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


MODULE_NAME = __name__


class SyncDocTermUsageModel(BaseTask):
    name = 'Synchronize Document Term Usage Summary'
    priority = 1

    SQL_INSERT = '''
    INSERT INTO "extract_documenttermusage" ("document_id", "term_id", "count")
    SELECT "document_textunit"."document_id", "extract_termusage"."term_id", 
        SUM("extract_termusage"."count") AS "count" 
    FROM "extract_termusage" 
    INNER JOIN "document_textunit" ON ("extract_termusage"."text_unit_id" = "document_textunit"."id") 
    GROUP BY "document_textunit"."document_id", "extract_termusage"."term_id" ORDER BY "count" DESC;
    '''

    SQL_CLEAR = 'DELETE FROM "extract_documenttermusage";'

    def process(self, **kwargs):
        self.log_info('Clearing Document Term Usage ...')
        with connection.cursor() as cursor:
            cursor.execute(self.SQL_CLEAR)

        self.log_info('Updating Document Term Usage ...')
        with connection.cursor() as cursor:
            cursor.execute(self.SQL_INSERT)


app.register_task(SyncDocTermUsageModel())