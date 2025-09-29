-- ======================================
-- Esquema de base de datos: Carta QR
-- ======================================

-- ==========================
-- Tabla Usuario
-- Cada usuario gestiona un solo negocio
-- ==========================
CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) NOT NULL
);

-- ==========================
-- Tabla Negocio
-- Relación 1:1 con Usuario
-- ==========================
CREATE TABLE Negocio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    usuario_id INT UNIQUE NOT NULL REFERENCES Usuario(id)
);

-- ==========================
-- Tabla Carta
-- Cada negocio puede tener hasta 2 cartas (control en backend)
-- ==========================
CREATE TABLE Carta (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    qr_url VARCHAR(255),
    negocio_id INT NOT NULL REFERENCES Negocio(id)
);

-- ==========================
-- Tabla Categoria
-- ==========================
CREATE TABLE Categoria (
    id SERIAL PRIMARY KEY,
    carta_id INT NOT NULL REFERENCES Carta(id)
);

-- ==========================
-- Tabla CategoriaTraduccion
-- Soporta varios idiomas
-- ==========================
CREATE TABLE CategoriaTraduccion (
    id SERIAL PRIMARY KEY,
    categoria_id INT NOT NULL REFERENCES Categoria(id),
    idioma VARCHAR(10) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    UNIQUE(categoria_id, idioma)
);

-- ==========================
-- Tabla Plato
-- Incluye precio y foto
-- ==========================
CREATE TABLE Plato (
    id SERIAL PRIMARY KEY,
    categoria_id INT NOT NULL REFERENCES Categoria(id),
    precio DECIMAL(10,2) NOT NULL,
    foto VARCHAR(255)
);

-- ==========================
-- Tabla PlatoTraduccion
-- Incluye descripción breve y una historia larga
-- ==========================
CREATE TABLE PlatoTraduccion (
    id SERIAL PRIMARY KEY,
    plato_id INT NOT NULL REFERENCES Plato(id),
    idioma VARCHAR(10) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion VARCHAR(300), -- breve
    historia TEXT,            -- historia larga
    UNIQUE(plato_id, idioma)
);

-- ==========================
-- Tabla Alergeno
-- Lista de alérgenos disponibles
-- ==========================
CREATE TABLE Alergeno (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    icono VARCHAR(255)
);

-- ==========================
-- Tabla PlatoAlergeno
-- Relación N:M entre Platos y Alérgenos
-- ==========================
CREATE TABLE PlatoAlergeno (
    plato_id INT NOT NULL REFERENCES Plato(id),
    alergeno_id INT NOT NULL REFERENCES Alergeno(id),
    PRIMARY KEY (plato_id, alergeno_id)
);
