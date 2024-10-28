import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { SecureApp } from "@asgardeo/auth-react";

// import Home from "../pages/Home";
import SideNavBar from "../pages/SideNavBar";
import { BaseLayout } from "../layouts/BaseLayout";

import { NotFoundPage } from "../pages/NotFound";
import { Loading } from "../pages/Loading";
import ProductListing from "../pages/ProductListing";
import Project from "../pages/Project";

const IndexRoutesWithAuth: React.FC = () => {
    return (
        <SecureApp fallback={<Loading />}>
            <Routes>
                <Route path="/side-nav-bars" element={<SideNavBar />} />
                <Route path="/sidenavex" element={<SideNavBar />} />
                <Route path="/home" element={<BaseLayout />}>
                    <Route index element={<Navigate to="/home" />} />
                    <Route path="projects" element={<ProductListing />} />
                    <Route path="sent" element={<Loading />} />
                    <Route path="project" element={<Project />} />
                </Route>

                <Route path="/loading" element={<Loading />} />
                <Route path="/NotFoundPage" element={<NotFoundPage />} />
            </Routes>
        </SecureApp>
    );
};

export default IndexRoutesWithAuth;
