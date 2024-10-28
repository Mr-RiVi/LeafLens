import { Grid } from '@mui/material';
import React from 'react';
import CardActionArea from '../../Card/CardActionArea'

import { gridCradData } from '../../../utils/GridCardData';
import CreateNewProductCard from '../../Card/CreateNewProductCard';

const ProductListingGrid: React.FC = () => {
    return (
        <Grid
            container
            rowSpacing={{ xs: 4, sm: 4, md: 4, lg: 4, xl: 4 }}
            columnSpacing={{ xs: 4, sm: 4, md: 4, lg: 4, xl: 4 }}
            columns={12}
            justifyContent="left"
        // style={{ maxWidth: '1500px', margin: '0 auto' }}
        >
            <Grid item xs={12} sm={6} md={3}>
                <CreateNewProductCard />
            </Grid>
            {gridCradData.map((data, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                    <CardActionArea
                        title={data.title}
                        description={data.description}
                    />
                </Grid>
            ))}
        </Grid>
    );
};

export default ProductListingGrid;
