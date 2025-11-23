async function importDataFast() {
    let connection;

    if (!fs.existsSync(csvFilePath)) {
        console.error(`Error: Archivo no encontrado en ${csvFilePath}`);
        console.error(`Ruta esperada: ${csvFilePath}`);
        return;
    }

    try {
        connection = await mysql.createConnection({ ...DB_CONFIG, localInfile: true });
        console.log('Conectado a MySQL.');

        // --- CORRECCIÓN CLAVE ---
        // 1. Preparamos la ruta para SQL (backslashes de Windows a forward slashes y escapes)
        const cleanPath = csvFilePath.replace(/\\/g, '/');
        const escapedPath = cleanPath.replace(/'/g, "\\'"); // Por si hay comillas en el path

        // 2. Insertamos la ruta escapada directamente en la cadena SQL (interpolación)
        const sql = `
            LOAD DATA LOCAL INFILE '${escapedPath}'
            INTO TABLE salud_mental
            FIELDS TERMINATED BY ',' 
            ENCLOSED BY '"'
            LINES TERMINATED BY '\\n'
            IGNORE 1 ROWS
            (
                @ANO,
                @Sexo_Gen,
                @edad_grupo_rias,
                @tipo_usuario_afiliacion,
                @prestador_localidad_codigo,
                @prestador_localidad_nombre,
                @tipo_atencion_nombre,
                @dxPrincipal_agrupacion1_nombre,
                @sum_atenciones
            )
            SET
                ANO = @ANO,
                Sexo_Gen = @Sexo_Gen,
                edad_grupo_rias = @edad_grupo_rias,
                tipo_usuario_afiliacion = @tipo_usuario_afiliacion,
                prestador_localidad_codigo = @prestador_localidad_codigo,
                prestador_localidad_nombre = @prestador_localidad_nombre,
                tipo_atencion_nombre = @tipo_atencion_nombre,
                dxPrincipal_agrupacion1_nombre = @dxPrincipal_agrupacion1_nombre,
                sum_atenciones = @sum_atenciones
        `;
        
        // 3. Ejecutamos el comando sin pasar un array de variables
        const [result] = await connection.execute(sql); 

        console.log('\n✅ Importación completada con LOAD DATA LOCAL INFILE.');
        console.log(`Filas insertadas: ${result.affectedRows}`);

    } catch (err) {
        console.error('❌ Error durante la importación:', err.message);
    } finally {
        if (connection) {
            await connection.end();
            console.log('Conexión MySQL cerrada.');
        }
    }
}