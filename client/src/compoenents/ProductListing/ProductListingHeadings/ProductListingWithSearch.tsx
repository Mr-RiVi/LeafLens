import { Box, IconButton, InputAdornment, styled, TextField, ThemeProvider, Typography } from '@mui/material';
import React, { useState } from 'react';

import RefreshOutlinedIcon from '@mui/icons-material/RefreshOutlined';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';

import useProductListingWithSearchTheme from '../../../assets/styles/Themes/ProductListing/ProductListingWithSearchTheme';

const ProductListingWithSearch: React.FC = () => {
    const [isSearchBarVisible, setIsSearchBarVisible] = useState(false);

    const ProductListingWithSearchTheme = useProductListingWithSearchTheme();

    const StyledRefreshIcon = styled(RefreshOutlinedIcon)(({ theme }) => ({
        fill: theme.palette.primary.main,
        width: '1em',
        height: '1em',
        display: 'inline-block',
        fontSize: '1.5rem',
        transition: 'fill 200ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
        flexShrink: 0,
        userSelect: 'none',

    }));

    return (
        <ThemeProvider theme={ProductListingWithSearchTheme}>
            <Box
                style={{
                    display: 'flex',
                    gap: '8px',
                    marginTop: '24px',
                    alignItems: 'center',
                    marginBottom: '24px',
                }}
            >
                <Typography variant="h2">All Projects</Typography>
                <Box>
                    <IconButton>
                        <StyledRefreshIcon />
                    </IconButton>
                </Box>
                <Box display="flex" justifyContent="flex-end" flexGrow={1} >
                    <IconButton onClick={() => setIsSearchBarVisible(!isSearchBarVisible)} >
                        {isSearchBarVisible ? <></> : <SearchOutlinedIcon />}
                    </IconButton>
                    {isSearchBarVisible && (
                        <TextField
                            placeholder="Search"
                            fullWidth
                            autoFocus
                            InputProps={{
                                disableUnderline: true,
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchOutlinedIcon />
                                    </InputAdornment>
                                ),
                                endAdornment: (
                                    <InputAdornment position="end">

                                        <IconButton onClick={() => setIsSearchBarVisible(false)}>
                                            <CloseOutlinedIcon />
                                        </IconButton>
                                    </InputAdornment>
                                ),
                            }}
                        />
                    )}
                </Box>

            </Box >
        </ThemeProvider>
    );
};

export default ProductListingWithSearch;