\c networks;

CREATE TABLE IF NOT EXISTS Graphs (
    GraphId INT PRIMARY KEY,
    InitialVertexIndex INT,
    FinalVertexIndex INT,
    IsDirected BOOLEAN,
    IsSimple BOOLEAN,
    GraphML TEXT
);