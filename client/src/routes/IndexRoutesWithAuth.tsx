import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { SecureApp } from "@asgardeo/auth-react";

// import Home from "../pages/Home";
import SideNavBar from "../pages/SideNavBar";
import Table from "../pages/Table";
// import DropdownMenu from "../pages/DropdownMenu";
import Cards from "../pages/Cards";
import Dialog from "../pages/Dialog";
import { BaseLayout } from "../layouts/BaseLayout";

import MiniDrawer from "../components/SideNavBars/tBar";
import { NotFoundPage } from "../pages/NotFound";
import { Loading } from "../pages/Loading";

import ManagerExample from "../pages/ManagerExample";
import EmployeeExample from "../pages/EmployeeExample";

import ExDataFetching from "../pages/ExDataFetching";
import ProductListing from "../pages/ProductListingPages/ProductListing";

const IndexRoutesWithAuth: React.FC = () => {
    return (
        <SecureApp fallback={<Loading />}>
            <Routes>
                {/* <Route path="/" element={<Home />} /> */}
                <Route path="/side-nav-bars" element={<SideNavBar />} />
                <Route path="/side" element={<MiniDrawer />} />
                <Route path="/sidenavex" element={<SideNavBar />} />
                <Route path="/tables" element={<Table />} />
                <Route path="/cards" element={<Cards />} />
                <Route path="/cards" element={<Cards />} />
                <Route path="/dialog" element={<Dialog />} />
                <Route path="/home" element={<BaseLayout />}>
                    <Route index element={<Navigate to="/home" />} />
                    <Route path="ex-data-fetching" element={<ExDataFetching />} />
                    <Route path="product-listing" element={<ProductListing />} />
                    <Route path="cards" element={<Cards />} />
                    <Route path="tables" element={<Table />} />
                    <Route path="sent" element={<Loading />} />
                </Route>

                <Route path="/manager" element={<ManagerExample />} />
                <Route path="/employee" element={<EmployeeExample />} />

                <Route path="/loading" element={<Loading />} />
                <Route path="/NotFoundPage" element={<NotFoundPage />} />
            </Routes>
        </SecureApp>
    );
};

export default IndexRoutesWithAuth;
