import React from 'react';

import ProductListingGrid from '../compoenents/ProductListing/ProductListingContents/ProductListingGrid';
import ProductListingWithSearch from '../compoenents/ProductListing/ProductListingHeadings/ProductListingWithSearch';
import { Box, Container } from '@mui/material';

const ProductListing: React.FC = () => {
    return (
        <Container
            style={{ maxWidth: '1500px', margin: '0 auto' }}
        >
            <Box>
                <ProductListingWithSearch />
                <ProductListingGrid />
            </Box>
        </Container>
    );
};

export default ProductListing;