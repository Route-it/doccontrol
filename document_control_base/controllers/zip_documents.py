# -*- encoding: utf-8 -*-
import zipfile
try:
    import zlib
    #compression = zlib.Z_BEST_COMPRESSION
    compression = zipfile.ZIP_DEFLATED
except:
    print 'error al importar zlib'
    compression = zipfile.ZIP_DEFLATED

from StringIO import StringIO
from openerp import http

class documentszip(http.Controller):
    #_cp_path = '/web/document_control_base/get_zip'
    
    @http.route('/web/document_control_base/getzip',type='http', auth='user')
    def index(self, req,  **kw):
        
        result = ''
        try:
            doc_set_id = int(kw['id'])
            doc_set = req.env['document_control_base.document_set'].search([('id','=',doc_set_id)])
           
            zip_file = StringIO()
            zf = zipfile.ZipFile(zip_file, mode='w',compression=compression)

            for doc in doc_set.document_set_document_rel_ids:
                document = False
                name = False
                if doc.document_id:
                    condition = [('res_id','=',doc.document_id.id),('res_model','=','document_control_base.document'),('res_field','=','file_binary')]
    
                    document = req.env['ir.attachment'].search(condition)
                    file_name_array = doc.document_id.file_name.split('.')
                    extension = file_name_array[len(file_name_array)-1]
                    
                    name =  doc.document_id.name.split(' - ')
                    name = name[0] + ' ' + name[1] + '.' + extension

                datas = document.datas.decode('base64') if document else "documento faltante"

                if not name: name = doc.res_partner_id.name + ' ' + doc.document_name_id.name +' (' + doc.state + ').txt'
                

                zf.writestr(name, datas, compression)
                
            zf.close()
            
            result = req.make_response(zip_file.getvalue(),headers=[
                                        ('Content-Disposition', 'attachment; filename="%s"'
                                            % doc_set.name+'.zip'),
                                        ('Content-Type', 'application/zip')
                                        ],
                                     cookies={}
                                     )
           
               
        except ValueError:
            result = req.make_response('',headers=[('refresh','0')],cookies={})

        #need to change every document_set_document_rel_ids state to "presented"
        # check if all docs are presented and change state of document_set to "cumplido" 

        return result
        

    """
    def getzip(self, req, data, token):
    def export_xls_view(self, data, token):
        data = json.loads(data)
        return req.make_response(
            self.from_data(data.get('headers', []), data.get('rows', [])),
                           headers=[
                                    ('Content-Disposition', 'attachment; filename="%s"'
                                        % data.get('model', 'Export.xls')),
                                    ('Content-Type', self.content_type)
                                    ],
                                 cookies={'fileToken': token}
                                 )



    """
