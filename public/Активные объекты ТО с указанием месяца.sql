SELECT DISTINCT
"public".maintenance_objects_to."id",
"public".reference_books_client."Name",
"public".maintenance_objects_to."AddressObject",
"public".maintenance_objects_to."Date_close",
"public".maintenance_objects_to."Date_open",
"public".reference_books_company."Name",
"public".maintenance_status_object."Name",
"public".reference_books_routesmaintenance."Descript",
"public".maintenance_objects_to."NumObject"
FROM
"public".maintenance_objects_to
INNER JOIN "public".reference_books_client ON "public".reference_books_client."id" = "public".maintenance_objects_to."Client_id"
INNER JOIN "public".reference_books_company ON "public".reference_books_company."id" = "public".maintenance_objects_to."ServingCompany_id"
INNER JOIN "public".maintenance_status_object ON "public".maintenance_status_object."id" = "public".maintenance_objects_to."Status_id"
INNER JOIN "public".reference_books_routesmaintenance ON "public".reference_books_routesmaintenance."id" = "public".maintenance_objects_to."Routes_id"
WHERE
"public".maintenance_objects_to."Status_id" = 1
ORDER BY
"public".reference_books_client."Name" ASC
