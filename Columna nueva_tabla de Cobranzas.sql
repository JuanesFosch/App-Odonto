--alter table Cargas_cobranzas  


update Cargas_cobranzas 
set Número_de_orden = (
	SELECT presupuestos_id
	from Cargas_cobranzas_Número_de_orden
	where Cargas_cobranzas_Número_de_orden.cobranzas_id = Cargas_cobranzas.Número_de_comprobante )
;

/*
update Cargas_cobranzas 
set Número_de_orden = Cargas_cobranzas_Número_de_orden.presupuestos_id 
from Cargas_cobranzas 
left join Cargas_cobranzas_Número_de_orden 
on Cargas_cobranzas.Número_de_comprobante = Cargas_cobranzas_Número_de_orden.cobranzas_id
;

select Cargas_cobranzas.Número_de_comprobante, Cargas_cobranzas.Fecha_de_cobro, 
Cargas_cobranzas.Cuánto_pagó, Cargas_cobranzas_Número_de_orden.presupuestos_id as Número_de_orden  
from Cargas_cobranzas

Left JOIN Cargas_cobranzas_Número_de_orden 
ON Cargas_cobranzas.Número_de_comprobante = Cargas_cobranzas_Número_de_orden.cobranzas_id 
;
*/