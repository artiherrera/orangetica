query_personas = """
SELECT
  p.id as P_ID,
  CONCAT(
    REGEXP_REPLACE(RTRIM(COALESCE(UPPER(p.name), '')), '[[:space:]]+$', ''),
    ' ',
    REGEXP_REPLACE(RTRIM(COALESCE(UPPER(p.first_surname), '')), '[[:space:]]+$', ''),
    ' ',
    REGEXP_REPLACE(RTRIM(COALESCE(UPPER(p.second_surname), '')), '[[:space:]]+$', '')
  ) AS "Persona",
  superior.id AS "ID Operador",
  CONCAT(
    REGEXP_REPLACE(RTRIM(COALESCE(UPPER(superior.name), '')), '[[:space:]]+$', ''),
    ' ',
    REGEXP_REPLACE(RTRIM(COALESCE(UPPER(superior.first_surname), '')), '[[:space:]]+$', ''),
    ' ',
    REGEXP_REPLACE(RTRIM(COALESCE(UPPER(superior.second_surname), '')), '[[:space:]]+$', '')
  ) AS "Operador",
  p.cellphone,
  p.elector_key AS "Clave de Elector",
  p.section AS "Sección",
  u.status AS "Estatus",
  COALESCE(NULLIF(nr.description, ''), 'Sin Responsabilidad') AS "Responsabilidad",
  COALESCE(NULLIF(nt.description,''), 'Presimpatizante') AS "Tipo",
  CAST(p.created_at AT TIME ZONE '-06:00' AS date) AS "Fecha de Alta",
  CAST(p.created_at AT TIME ZONE '-06:00' AS time) AS "Hora de Alta",
  CAST(p.updated_at AT TIME ZONE '-06:00' AS date) AS "Fecha de cambio",
  CAST(p.updated_at AT TIME ZONE '-06:00' AS time) AS "Hora de cambio"
FROM
  public.person p
JOIN
  "user" u ON p.user_id = u.id
LEFT JOIN LATERAL (
  SELECT *
  FROM person superior
  WHERE superior.user_id = u.superior_id
) superior ON true
LEFT JOIN nom_responsibility nr ON u.responsibility_id = nr.id
LEFT JOIN nom_type nt ON u.type_id = nt.id
LEFT JOIN role r ON u.role_id = r.id
ORDER BY superior.id
"""
