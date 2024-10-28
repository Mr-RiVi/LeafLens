/* The navigation drawers (or "sidebars") provide ergonomic access to destinations
 in a site or app functionality such as switching accounts. */

import React, { FunctionComponent, ReactElement } from "react";
import { Link } from "react-router-dom";

import MuiDrawer from '@mui/material/Drawer';

import {
  Box,
  CSSObject,
  Collapse,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Theme,
  ThemeProvider,
  Toolbar,
  styled,
  useTheme,
} from "@mui/material";

import ExpandLessOutlinedIcon from '@mui/icons-material/ExpandLessOutlined';
import ExpandMoreOutlinedIcon from '@mui/icons-material/ExpandMoreOutlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import ArrowForwardIosOutlinedIcon from '@mui/icons-material/ArrowForwardIosOutlined';
import ArrowBackIosOutlinedIcon from '@mui/icons-material/ArrowBackIosOutlined';

import { DrawerTheme } from "../../assets/styles/Themes/CustomDrawerTheme";


const drawerWidth = 212;

const themedStyles = (theme: Theme) => {
  return {
    sidebar: {
      "& .MuiBackdrop-root": {
        display: "none"
      },
      [`& .MuiDrawer-paper`]: {
        background: theme.palette.primary.main
      }
    }
  }
}

const openedMixin = (theme: Theme): CSSObject => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(6)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(7)} + 1px)`,
  },
});

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

/**
 * The NavItemProps type defines the structure of an individual navigation item.
 * It includes properties icon, label (text for the link), link (URL for the link),
 * and subItems (optional array of nested navigation items). *
 */
type NavItemProps = {
  icon?: React.ReactNode;
  label: string;
  link?: string | undefined;
  subItems?: NavItemProps[];
};

/**
 * NavItem Component:
 * This component represents an individual navigation item.
 *
 * @param {NavItemProps} item - The data for the current navigation item.
 */
const NavItem: FunctionComponent<{ item: NavItemProps }> = ({ item }): ReactElement => {
  const [openSubItems, setOpenSubItems] = React.useState(true);

  const handleItemClick = () => {
    setOpenSubItems(!openSubItems);
  };
  return (
    <List>
      {item.subItems ? (
        <>
          <Box>
            <ListItemButton onClick={handleItemClick}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
              {item.subItems && (!openSubItems ? <ExpandLessOutlinedIcon /> : <ExpandMoreOutlinedIcon />)}
            </ListItemButton>
            <Collapse in={!openSubItems} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {item.subItems?.map((subItem) => (
                  <Link
                    to={subItem.link || ""}
                    style={{ textDecoration: "none" }}
                  >
                    <ListItemButton sx={{ pl: 4 }}>
                      <ListItemIcon>{subItem.icon}</ListItemIcon>
                      <ListItemText primary={subItem.label} />
                    </ListItemButton>
                  </Link>
                ))}
              </List>
            </Collapse>
          </Box>
        </>
      ) : (
        <Link
          to={item.link || ""}
          style={{
            textDecoration: "none"
          }}
        >
          <ListItemButton onClick={handleItemClick}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        </Link>
      )}
    </List>
  );
};

/**
 * The NavBarProps type defines the props that the NavBar component expects.
 * It includes a property named items, which is an array of NavItem objects.
 */
type NavBarProps = {
  items: NavItemProps[];
};

/**
 * NavBar Component:
 * This component represents a navigation bar that displays a list of items.
 *
 * @param {NavBarProps} items - The array of navigation items to be displayed.
 */
export default function MuiExpandableSidebar({ items }: NavBarProps) {
  const [open, setOpen] = React.useState(false);

  const theme = useTheme()

  const handleDrawerToggle = () => {
    setOpen(!open);
  };

  return (
    <ThemeProvider theme={DrawerTheme}>
      <Box sx={{ ...themedStyles(theme).sidebar }}>
        <Drawer
          variant="permanent"
          anchor="left"
          open={open}
        >
          <Box
          // sx={{ padding: 1 }}
          >
            {/* used this toolbar comp to get space cz of appbar component */}
            <Toolbar />
            {/* Map through the array of items and render a NavItem component for each */}
            {items.map((item, index) => (
              <NavItem key={index} item={item} />
            ))}
          </Box>
          <Box style={{ marginTop: "auto" }}>
            {/* Settings button */}
            <List>
              <Link
                to={"/settings"}
                style={{ textDecoration: "none" }}
              >
                <ListItemButton>
                  <ListItemIcon>{<SettingsOutlinedIcon />}</ListItemIcon>
                  <ListItemText primary={"Settings"} />
                </ListItemButton>
              </Link>
            </List>

            {/* Expand and Collaps button */}
            <Divider />
            <List>
              <ListItemButton onClick={handleDrawerToggle}>
                <ListItemIcon>{open ? <ArrowBackIosOutlinedIcon /> : <ArrowForwardIosOutlinedIcon />}</ListItemIcon>
                <ListItemText primary={open ? "Collapse" : "Expand"} />
              </ListItemButton>
            </List>
          </Box>

        </Drawer >
      </Box>
    </ThemeProvider>
  );
}
