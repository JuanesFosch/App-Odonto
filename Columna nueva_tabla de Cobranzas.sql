--alter table Cargas_cobranzas  


update Cargas_cobranzas 
set N�mero_de_orden = (
	SELECT presupuestos_id
	from Cargas_cobranzas_N�mero_de_orden
	where Cargas_cobranzas_N�mero_de_orden.cobranzas_id = Cargas_cobranzas.N�mero_de_comprobante )
;

/*
update Cargas_cobranzas 
set N�mero_de_orden = Cargas_cobranzas_N�mero_de_orden.presupuestos_id 
from Cargas_cobranzas 
left join Cargas_cobranzas_N�mero_de_orden 
on Cargas_cobranzas.N�mero_de_comprobante = Cargas_cobranzas_N�mero_de_orden.cobranzas_id
;

select Cargas_cobranzas.N�mero_de_comprobante, Cargas_cobranzas.Fecha_de_cobro, 
Cargas_cobranzas.Cu�nto_pag�, Cargas_cobranzas_N�mero_de_orden.presupuestos_id as N�mero_de_orden  
from Cargas_cobranzas

Left JOIN Cargas_cobranzas_N�mero_de_orden 
ON Cargas_cobranzas.N�mero_de_comprobante = Cargas_cobranzas_N�mero_de_orden.cobranzas_id 
;
*/