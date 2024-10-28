import React, { FunctionComponent, ReactElement } from "react";

import { useAuthContext } from "@asgardeo/auth-react";

import {
    AppBar,
    Avatar,
    Box,
    Divider,
    IconButton,
    ListItem,
    ListItemAvatar,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Menu,
    MenuList,
    Theme,
    ThemeProvider,
    Toolbar,
    Typography,
    useTheme
} from "@mui/material";

import AttractionsOutlinedIcon from '@mui/icons-material/AttractionsOutlined';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';

import { AppBarTheme } from "../../assets/styles/Themes/CustomAppBarTheme";
import useProfileMenuTheme from "../../assets/styles/Themes/customProfileMenuTheme";

const themedStyles = (theme: Theme) => {
    return {
        avatarContainer: {
            width: 32,
            height: 32,
            position: 'relative',
            display: 'inline-block',
            border: `2px solid ${theme.palette.primary.main}`,
            borderRadius: '50%',
            overflow: 'hidden',
            transition: 'border-color 0.2s ease-in-out'
        },
        menuAvatar: {
            width: 40,
            height: 40,
            border: '1px solid white',
            fontSize: 13
        }
    }
}

/**
 * Component to display for header section.
 *
 * @param props - Props injected to the component.
 *
 * @return {React.ReactElement}
 */
export const Header: FunctionComponent = (): ReactElement => {
    const { signOut, state } = useAuthContext();

    const pic_url = "";
    const displayName = state.displayName;
    const username = state.username;

    const theme = useTheme();
    const profileMenuTheme = useProfileMenuTheme();

    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        console.log(state);
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        signOut();
    }

    return (
        <ThemeProvider theme={AppBarTheme}>
            <AppBar
                elevation={0}
                position="fixed"
            >
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{
                            color: "black",
                            flexGrow: 1
                        }}
                    >
                        Logo
                    </Typography>
                    {state.isAuthenticated && (
                        <ThemeProvider theme={profileMenuTheme}>
                            <Box>
                                <Box>
                                    <IconButton
                                        size="large"
                                        aria-label="account of current user"
                                        aria-controls="menu-appbar"
                                        aria-haspopup="true"
                                        onClick={handleMenu}
                                        color="inherit"
                                    >
                                        <Box
                                            sx={{
                                                ...themedStyles(theme).avatarContainer
                                            }}>
                                            <Avatar
                                                alt={displayName}
                                                src={pic_url}
                                            />
                                        </Box>
                                    </IconButton>
                                </Box>
                                <Menu
                                    id="menu-appbar"
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={Boolean(anchorEl)}
                                    onClose={handleClose}
                                    sx={{ mt: '45px' }}
                                >
                                    <MenuList
                                        sx={{ padding: 0 }}
                                    >
                                        <ListItem>
                                            <ListItemAvatar>
                                                <Avatar
                                                    alt={displayName}
                                                    src={pic_url}
                                                    sx={{ ...themedStyles(theme).menuAvatar }}
                                                />
                                            </ListItemAvatar>
                                            <ListItemText primary={displayName} secondary={username} />
                                        </ListItem>
                                        <Box sx={{ paddingTop: '8px' }}>
                                            <Divider />
                                        </Box>
                                        <ListItemButton
                                            onClick={handleClose}
                                        >
                                            <ListItemIcon
                                            >
                                                <SettingsOutlinedIcon />
                                            </ListItemIcon>
                                            <ListItemText primary="Feature Preview" />
                                        </ListItemButton>
                                        <ListItemButton
                                            onClick={handleClose}
                                        >
                                            <ListItemIcon
                                            >
                                                <AttractionsOutlinedIcon />
                                            </ListItemIcon>
                                            <ListItemText primary="Profile" />
                                        </ListItemButton>
                                        <ListItemButton
                                            onClick={handleLogout}
                                        >
                                            <ListItemIcon
                                            >
                                                <LogoutOutlinedIcon />
                                            </ListItemIcon>
                                            <ListItemText primary="Logout" />
                                        </ListItemButton>
                                    </MenuList>
                                </Menu>
                            </Box>
                        </ThemeProvider>
                    )}
                </Toolbar>
                <Divider />
            </AppBar>
        </ThemeProvider>
    );
};