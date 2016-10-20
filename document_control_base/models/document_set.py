# -*- coding: utf-8 -*-

from openerp import models, fields, api


class document_set(models.Model):
    _name = 'document_control_base.document_set'
     
    name = fields.Char("Nombre")
     
    description = fields.Text('Descripcion')

    group_requirement_id = fields.Many2one("document_control_base.group_requirement", "Grupo de Requerimientos")
    
    partner_ids = fields.Many2many("res.partner","document_set_partner_rel", "document_set_id", "partner_id", "Recursos Involucrados")

    document_set_document_rel_ids = fields.One2many("document_control_base.document_set_document_rel", "document_set_id", 
                                                    "Documentos",readonly=True,ondelete='cascade')

    control_date = fields.Many2one("calendar.event",string="Fecha de control")
    
    """
    def get_d_set_d_rel(self,req_id,partner):
        for x in self.document_set_document_rel_ids:
            if (x.res_partner_id.id == partner) & (x.requirement_id.id == req_id):
                return x
    """

    def get_documents_to_present(self):
        #retorna la lista de documentos a presentar (para firmar por el cliente)
        return


    def get_resources(self):
        return self.partner_ids


    
    @api.one
    def compute_document_set_document_rel(self):
        print 'onchange_group_requirement'
        res = []
        d_set_d_rel_obj = self.env['document_control_base.document_set_document_rel']
        g_req_req_rel_obj = self.env['document_control_base.group_req_requirement_rel']

        resources = self.get_resources()
        
        requirement_ids = [x.id for x in self.group_requirement_id.requirement_ids]

        #eliminar los dsdr que no sean requerimientos (no estan en requirement_ids
        d_set_d_rel_to_delete = d_set_d_rel_obj.search([('document_set_id','=',self.id),('requirement_id','not in', requirement_ids)])
        for x in d_set_d_rel_to_delete:
            super(document_set, self).write({'document_set_document_rel_ids':[(2, x.id, False)]})

        #eliminar los dsdr que tengan resources que no esten en resource_ids
        print "Eliminar docs de resources que no estan en lista"
        resource_ids = [(x._name,x.id) for x in resources]
        
        result_dict = {}
        for x in resource_ids:
            if x[0] not in result_dict:
                result_dict[x[0]] = []
            result_dict[x[0]].append(x[1])

        
        d_set_d_rel_exist_ni = []
        for x in result_dict.keys():
                property_name = x.replace(".","_")+"_id"
                d_set_d_rel_exist_ni +=  d_set_d_rel_obj.search([('document_set_id','=',self.id),('requirement_id','in', requirement_ids),(property_name,'not in',result_dict.get(x))])
                #d_set_d_rel_exist_ni +=  d_set_d_rel_obj.search([('document_set_id','=',self.id),('requirement_id','=', group_req_req_rel.requirement_id.id),(property_name,'not in',result_dict.get(x))])

        for x in d_set_d_rel_exist_ni:
            super(document_set, self).write({'document_set_document_rel_ids':[(2, x.id, False)]})


        #por cada requerimiento
        for req_id in self.group_requirement_id.requirement_ids:
            group_req_req_rel = g_req_req_rel_obj.search([('requirement_id','=',req_id.requirement_id.id),('group_requirement_id','=',self.group_requirement_id.id)])
            
            #por cada partner
            if len(resources)>0:
                for resource in resources:
                    if resource._name == req_id.requirement_id.resource_type:
                        #busco si existe el registro para el requerimiento & resource
                        property_name = resource._name.replace(".","_")+"_id"
                        
                        d_set_d_rel_exist = d_set_d_rel_obj.search([('document_set_id','=',self.id),('requirement_id','=', req_id.requirement_id.id),(property_name,'=',resource.id)])
                        #d_set_d_rel_exist = self.search_d_set_d_rel_with_res([('document_set_id','=',self.id),('requirement_id','=', req_id.requirement_id.id)],resource)
                        
                        # si hay mas de 1 registro que cumple (no deberia darse el caso), borro el resto que esta de mas. (con 1 alcanza)
                        if len(d_set_d_rel_exist)>1:
                            size = len(d_set_d_rel_exist)
                            for x in range(1,size):
                                super(document_set, self).write({'document_set_document_rel_ids':[(2, d_set_d_rel_exist[x].id, False)]})
                            d_set_d_rel_exist = d_set_d_rel_exist[0]
                        
                        #si el resource, reune las condiciones del requerimiento,  
                        # o, el resource cumple con todas las condiciones
                        #if len(resource.resource_condition_ids - req_id.requirement_id.condition_res_ids) == 0:
                        defaults = {property_name:resource.id,'requirement_id':group_req_req_rel.requirement_id.id,'document_name_id':group_req_req_rel.requirement_id.document_name_id.id}
                        defaults.update({'res_type':req_id.requirement_id.resource_type})  

                        if not bool(group_req_req_rel.priority):
                            group_req_req_rel.priority = 'normal'
                            group_req_req_rel._compute_name()
                            
                        priority = str(group_req_req_rel.priority) 
                        defaults.update({'priority':priority})  
                        #if (group_req_req_rel.requirement_id.condition_res_ids <= resource.resource_condition_ids):
                        if (len(group_req_req_rel.requirement_id.condition_res_ids - resource.resource_condition_ids) == 0):
                            doc_added = False
                            defaults.update({'document_set_id':self.id})
                            #defaults = self.add_resource_id(defaults, resource)
                              
                            if len(resource.document_ids)>0:
                                for doc in resource.document_ids:
                                    #busco el documento del resource que cumpla con las condiciones
                                    #'document_set_id':self.id,
                                    if (doc.document_name_id == group_req_req_rel.requirement_id.document_name_id): 
                                        if (len(doc.document_condition_ids - group_req_req_rel.requirement_id.condition_doc_ids)==0):
                                            #Si existe el documento, y reune las condicioneslo agregamos a la lista. 
                                            #crear un document_set_document_rel
                                            defaults.update({'document_id':doc.id})
                                            """
                                            (0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
                                            (1, ID, { values })    update the linked record with id = ID (write *values* on it)
                                            (2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
        
                                            Example:
                                               [(0, 0, {'field_name':field_value_record1, ...}), (0, 0, {'field_name':field_value_record2, ...})]
                                            """
                                            
                                            if not d_set_d_rel_exist:
                                                #computed_ids.append(target.id)
                                                super(document_set, self).write({'document_set_document_rel_ids':[(0, 0, defaults)]})
                                                print 'create d_set_d_rel' + str(d_set_d_rel_exist)
                                            else:
                                                #update
                                                #self.document_set_document_rel_ids |=  self.env['document_control_base.document_set_document_rel'].create(defaults)
                                                print 'update d_set_d_rel' + str(d_set_d_rel_exist[0])
                                                super(document_set, self).write({'document_set_document_rel_ids':[(1, d_set_d_rel_exist.id, defaults)]})
                                        else:
                                            # encontre el documento pero no reune las condiciones
                                            print 'encontre el documento pero no reune las condiciones'
                                            if not d_set_d_rel_exist:
                                                print 'create missing'
                                                super(document_set, self).write({'document_set_document_rel_ids':[(0, 0, defaults)]})
                                            else:
                                                print 'update missing'
                                                super(document_set, self).write({'document_set_document_rel_ids':[(1, d_set_d_rel_exist.id, defaults)]})
                                        doc_added = True
                                    else:
                                            #No es el documento en cuestion, se ignora
                                            print 'No es el documento en cuestion, se ignora'
                            else:
                                #el resource no tiene documentos.
                                print 'el resource no tiene documentos.'
                                doc_added = True                        
                                if not d_set_d_rel_exist:
                                    print 'create missing.'
                                    super(document_set, self).write({'document_set_document_rel_ids':[(0, 0, defaults)]})
                                else:
                                    print 'update missing.'
                                    super(document_set, self).write({'document_set_document_rel_ids':[(1, d_set_d_rel_exist.id, defaults)]})
                            
                            #chequear si se updateo o creo un doc. Sino, agregar un missing
                            if not (doc_added):
                                if not d_set_d_rel_exist:
                                    print 'create missing'
                                    super(document_set, self).write({'document_set_document_rel_ids':[(0, 0, defaults)]})
                                else:
                                    print 'update missing'
                                    super(document_set, self).write({'document_set_document_rel_ids':[(1, d_set_d_rel_exist.id, defaults)]})
                                
                        else:
                            #self.document_set_document_rel_ids |=  self.env['document_control_base.document_set_document_rel'].create(defaults)
                            print "el resource no reune las condiciones."
                            if d_set_d_rel_exist:
                                print "borrar entrada de resource que no aplica."
                                super(document_set, self).write({'document_set_document_rel_ids':[(2, d_set_d_rel_exist.id, False)]})
                    else:
                        print "comparando peras con manzanas"

            else:
                #Si no hay recursos, remover todos los documentos
                #d_set_d_rel_exist = d_set_d_rel_obj.search([('document_set_id','=',self.id),('requirement_id','=', req_id.requirement_id.id)])
                print 'Si no hay recursos, remover todos los documentos'
                for x in self.document_set_document_rel_ids:
                    super(document_set, self).write({'document_set_document_rel_ids':[(2, x.id, False)]})

        return res

                            
        """
            PSEUDOCODIGO
            
        for req_id in group_requirement_id.requirement_ids
                req_id
                    {document_name_id,
                    condition_doc_ids,
                    resource_type,
                    condition_res_ids
                    } 
                tomar req_id.resource type y req_id.condition_res_ids
                for partner in self.partner_ids(segun resource_type), 
                    if (partner.resource_condition_ids contains all req_id.condition_res_ids):
                        for doc in documents_ids:
                            si cumple con requirement_id.document_name_id && condition_doc_ids
                                crear/updatear un document_set_document_rel
                                    {document_id,res_partner_id}
                            si no cumple:
                                crear/updatear un document_set_document_rel
                                    {res_partner_id} //documento faltante

                si hay mas document_set_document_rel que group_requirement_id.requirement_ids
                    para cada document_set_document_rel:
                         tomar {document_name_id,partner_id} y buscarlo en group_requirement_id.requirement_ids
                             Si no lo encuentra, borrarlo.
                             Si lo encuentra continuar.
        
        """
        #res = []
        #res.append({'document_set_document_rel_ids':""})
                   
#                    'tax_ids': [(6, 0, done_taxes)] if tax_line.tax_id.include_base_amount else []
        #return res
    
        #return 
    """    
    @api.model
    def create(self,values):
        res = super(document_set, self).create( values)

        self._compute_document_set_document_rel()

        return res

    """

    @api.multi
    def write(self, values):
        #update all other values
        res = super(document_set, self).write(values)
        #calculate new documentt related
        self.compute_document_set_document_rel()
        
        #write that documents.
        #res = super(document_set, self).write(values)

        return res
    
    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        #your changes
        default.update(name="%s (copy)" % (self.name or ''))
        
        result = super(document_set, self).copy(default)
        
        
        """
        # copy collections fields        
        
        map_task_id = {}
        task_obj = self.pool.get('project.task')
        proj = self.browse(cr, uid, old_project_id, context=context)
        for task in proj.tasks:
            # preserve task name and stage, normally altered during copy
            defaults = {'stage_id': task.stage_id.id,
                        'name': task.name}
            map_task_id[task.id] =  task_obj.copy(cr, uid, task.id, defaults, context=context)
        self.write(cr, uid, [new_project_id], {'tasks':[(6,0, map_task_id.values())]})
        task_obj.duplicate_task(cr, uid, map_task_id, context=context)
        
        
        """
        return result
        
