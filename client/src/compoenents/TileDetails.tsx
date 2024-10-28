import { Box, Grid, Paper, Typography } from '@mui/material';
import * as React from 'react';

const TileDetails: React.FC<{}> = ({ }) => {
    return (
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
    );
}

export default TileDetails;