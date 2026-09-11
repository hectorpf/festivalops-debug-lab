PRAGMA foreign_keys = ON;

CREATE TABLE stages (
    stage_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    genre TEXT NOT NULL
);

CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    stage_id INTEGER NOT NULL REFERENCES stages(stage_id),
    artist_id INTEGER NOT NULL REFERENCES artists(artist_id),
    starts_at TEXT NOT NULL,
    ends_at TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE ticket_sales (
    sale_id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    unit_price TEXT NOT NULL
);

CREATE TABLE incidents (
    incident_id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id),
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO stages VALUES
    (1, 'Escenario Principal', 1000),
    (2, 'Escenario Río', 600),
    (3, 'Escenario Bosque', 350);

INSERT INTO artists VALUES
    (1, 'Luz de Barrio', 'Indie'),
    (2, 'The Cats, Live', 'Rock'),
    (3, 'Neón Atlántico', 'Electrónica'),
    (4, 'Mar Abierto', 'Pop'),
    (5, 'Ritmo Norte', 'Urbano'),
    (6, 'Bosque Sonoro', 'Folk'),
    (7, 'Medianoche Club', 'Electrónica'),
    (8, 'Voces del Río', 'Soul');

INSERT INTO events VALUES
    (101, 1, 1, '2026-07-10T18:00:00', '2026-07-10T19:30:00', 'programado'),
    (102, 1, 2, '2026-07-10T21:00:00', '2026-07-10T22:30:00', 'programado'),
    (103, 1, 3, '2026-07-10T23:30:00', '2026-07-11T01:00:00', 'programado'),
    (104, 2, 4, '2026-07-10T19:00:00', '2026-07-10T20:15:00', 'programado'),
    (105, 2, 5, '2026-07-10T22:00:00', '2026-07-10T23:15:00', 'programado'),
    (106, 2, 7, '2026-07-11T00:30:00', '2026-07-11T02:00:00', 'programado'),
    (107, 3, 6, '2026-07-10T18:30:00', '2026-07-10T19:45:00', 'programado'),
    (108, 3, 8, '2026-07-10T20:30:00', '2026-07-10T21:45:00', 'programado');

INSERT INTO ticket_sales VALUES
    (1, 101, 300, '25.00'),
    (2, 101, 200, '25.00'),
    (3, 102, 600, '40.00'),
    (4, 102, 400, '40.00'),
    (5, 103, 200, '30.00'),
    (6, 104, 350, '22.50'),
    (7, 105, 410, '27.00'),
    (8, 106, 280, '31.00'),
    (9, 107, 350, '19,90'),
    (10, 108, 180, '24.00');

INSERT INTO incidents VALUES
    (1, 101, 'media', 'abierta', 'Cola lenta en el acceso norte'),
    (2, 101, 'baja', 'abierta', 'Señalización poco visible'),
    (3, 103, 'alta', 'cerrada', 'Reinicio del sistema de luces'),
    (4, 105, 'media', 'abierta', 'Retraso de diez minutos'),
    (5, 106, 'alta', 'abierta', 'Cambio de acceso por lluvia');
