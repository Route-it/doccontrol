-- Table: document_control_base_group_req_requirement_rel

-- DROP TABLE document_control_base_group_req_requirement_rel;

CREATE TABLE document_control_base_group_req_requirement_rel
(
  id serial NOT NULL,
  create_uid integer, -- Created by
  create_date timestamp without time zone, -- Created on
  name character varying, -- Nombre
  penalty text, -- Penalidad
  write_uid integer, -- Last Updated by
  priority character varying, -- Prioridad
  write_date timestamp without time zone, -- Last Updated on
  group_requirement_id integer, -- Grupo de Requerimientos
  requirement_id integer, -- Requerimiento
  CONSTRAINT document_control_base_group_req_requirement_rel_pkey PRIMARY KEY (id),
  CONSTRAINT document_control_base_group_req_requi_group_requirement_id_fkey FOREIGN KEY (group_requirement_id)
      REFERENCES document_control_base_group_requirement (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT document_control_base_group_req_requirement_rel_create_uid_fkey FOREIGN KEY (create_uid)
      REFERENCES res_users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT document_control_base_group_req_requirement_rel_write_uid_fkey FOREIGN KEY (write_uid)
      REFERENCES res_users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL,
  CONSTRAINT document_control_base_group_req_requirement_requirement_id_fkey FOREIGN KEY (requirement_id)
      REFERENCES document_control_base_requirement (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE document_control_base_group_req_requirement_rel
  OWNER TO openpg;
COMMENT ON TABLE document_control_base_group_req_requirement_rel
  IS 'document_control_base.group_req_requirement_rel';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.create_uid IS 'Created by';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.create_date IS 'Created on';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.name IS 'Nombre';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.penalty IS 'Penalidad';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.write_uid IS 'Last Updated by';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.priority IS 'Prioridad';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.write_date IS 'Last Updated on';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.group_requirement_id IS 'Grupo de Requerimientos';
COMMENT ON COLUMN document_control_base_group_req_requirement_rel.requirement_id IS 'Requerimiento';

