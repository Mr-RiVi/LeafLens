import { FunctionComponent, PropsWithChildren, ReactElement } from "react";

// import MuiSideNav from "../components/SideNavBars/MuiSideNav";

import ViewQuiltOutlinedIcon from '@mui/icons-material/ViewQuiltOutlined';
import DatasetOutlinedIcon from '@mui/icons-material/DatasetOutlined';
import DataUsageIcon from '@mui/icons-material/DataUsage';
import SendOutlinedIcon from '@mui/icons-material/SendOutlined';
import StarBorderOutlinedIcon from '@mui/icons-material/StarBorderOutlined';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';

import MuiExpandableSidebar from "../compoenents/SideNavBars/MuiExpandableSidebar";

interface SideNavBarPropsInterface { }

const SideNavBar: FunctionComponent<
  PropsWithChildren<SideNavBarPropsInterface>
> = (): ReactElement => {
  const navItems = [
    {
      icon: <DataUsageIcon />,
      label: "Dashboard",
      link: "/home/ex-data-fetching",
    },
    {
      icon: <DatasetOutlinedIcon />,
      label: "Projects",
      link: "/home/projects",
    },
    {
      icon: <SendOutlinedIcon />,
      label: "Sent Items",
      link: "/home/sent",
    },
    {
      icon: <StarBorderOutlinedIcon />,
      label: "Project",
      link: "/home/project",
    },
    {
      icon: <DeleteOutlinedIcon />,
      label: "Trash",
      link: "/trash",
    },
    {
      icon: <ViewQuiltOutlinedIcon />,
      label: "Custom Section",
      subItems: [
        {
          icon: <StarBorderOutlinedIcon />,
          label: "Important",
          link: "/important",
        },
        {
          icon: <DeleteOutlinedIcon />,
          label: "Deleted",
          link: "/deleted",
        },
      ],
    },
  ];

  return (
    <>
      {/* <MuiSideNav items={navItems} /> */}
      <MuiExpandableSidebar items={navItems} />

    </>
  );
};

export default SideNavBar;
