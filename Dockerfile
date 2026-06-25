# Imagen base oficial de Odoo 16
FROM odoo:16.0

# Copiamos los tres módulos del club de pádel dentro del contenedor
COPY ./club_padel /mnt/extra-addons/club_padel
COPY ./club_padel_tienda /mnt/extra-addons/club_padel_tienda
COPY ./tienda_padel /mnt/extra-addons/tienda_padel

# Odoo escucha en el puerto 8069
EXPOSE 8069

# Comando que mantiene el contenedor vivo sirviendo la aplicación web
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"]
