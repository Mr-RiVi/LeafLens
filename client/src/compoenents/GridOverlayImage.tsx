import { Box, Grid, Paper, Typography } from '@mui/material';
import * as React from 'react';

type TileDetails = {
    id: number;
    description: string;
    // Add more fields based on API response
};

type TileData = {
    id: number;
    image: string; // URL or base64 string for the tile image
    mean: number;
    stdDev: number;
    min: number;
    max: number;
};

const GridOverlayImage: React.FC<{}> = ({ }) => {
    const [open, setOpen] = React.useState(false);
    const [loading, setLoading] = React.useState(false);
    const [selectedTile, setSelectedTile] = React.useState<TileData | null>(null);

    const fetchTileDetails = async (id: number) => {
        setLoading(true);
        try {
            // Make an API call to get details for the specific tile
            const response = await fetch(`/api/tile-details/${id}`);
            const data = await response.json();
            setSelectedTile(data);
        } catch (error) {
            console.error("Failed to fetch tile details:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleTileClick = (id: number) => {
        setOpen(true);
        fetchTileDetails(id);
    };

    return (
        <Grid container spacing={2} sx={{ width: "100%", height: '100vh', padding: 2 }}>
            <Box
                sx={{
                    position: "relative",
                    display: "inline-block",
                    border: "1px solid #ddd",
                    borderRadius: 2,
                    overflow: "hidden",
                }}
            >
                {/* Display Background Image */}
                <Box
                    component="img"
                    src="/src/assets/images/screenshot333.jpeg"
                    alt="Tea Estate"
                    sx={{
                        width: "100%",
                        height: "auto",
                        opacity: 0.9,
                    }}
                />

                {/* Grid Overlay */}
                <Box
                    sx={{
                        position: "absolute",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        display: "grid",
                        gridTemplateColumns: "repeat(10, 1fr)", // Adjust to the number of columns
                        gridTemplateRows: "repeat(7, 1fr)", // Adjust to the number of rows
                    }}
                >
                    {[...Array(7 * 10)].map((_, index) => (
                        <Box
                            key={index}
                            sx={{
                                border: "1px solid rgba(255, 255, 255, 0.5)",
                                cursor: "pointer",
                                "&:hover": {
                                    backgroundColor: "rgba(255, 255, 255, 0.3)",
                                },
                            }}
                            onClick={() => handleTileClick(index + 1)}
                        />
                    ))}
                </Box>
            </Box>

            <Grid item xs={4}>
                <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
                    {selectedTile ? (
                        <Box>
                            <Typography variant="h6">Tile Details</Typography>
                            <Box
                                component="img"
                                src={selectedTile.image}
                                alt="Tile Image"
                                sx={{ width: '100%', height: 'auto', marginBottom: 2 }}
                            />
                            <Typography variant="body1">Mean: {selectedTile.mean}</Typography>
                            <Typography variant="body1">Standard Deviation: {selectedTile.stdDev}</Typography>
                            <Typography variant="body1">Min: {selectedTile.min}</Typography>
                            <Typography variant="body1">Max: {selectedTile.max}</Typography>
                        </Box>
                    ) : (
                        <Typography variant="body1">Select a tile to view details.</Typography>
                    )}
                </Paper>
            </Grid>
        </Grid>
    );
}

export default GridOverlayImage;