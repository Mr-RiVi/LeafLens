import * as React from 'react';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import { CardActionArea, useTheme } from '@mui/material';

import AddOutlinedIcon from '@mui/icons-material/AddOutlined';
import ProductCreationDialog from '../Dialog/ProductCreationDialog';

const CreateNewProductCard: React.FC = () => {
    const [isDialogOpen, setDialogOpen] = React.useState<boolean>(false);
    console.log(isDialogOpen);

    const theme = useTheme();
    return (
        <Card sx={{ maxWidth: 345, height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', border: `1px solid ${theme.palette.primary.main}` }}>
            <CardActionArea
                sx={{ textAlign: 'center', height: '100%' }}
                onClick={() => setDialogOpen(true)}
            >
                <AddOutlinedIcon style={{ color: theme.palette.primary.main }} />
                <Typography
                    style={{ color: theme.palette.primary.main }}
                    variant="h6"
                >
                    Create Project
                </Typography>
            </CardActionArea>
            <ProductCreationDialog
                open={isDialogOpen}
                onClose={setDialogOpen}
                content={{ hello: 12 }}
            />
        </Card>
    );
}

export default CreateNewProductCard;