import { FunctionComponent, ReactElement } from "react";
import "../assets/styles/loading.css";

/**
 * Page to display for Loading.
 *
 * @param props - Props injected to the component.
 *
 * @return {React.ReactElement}
 */
export const Loading: FunctionComponent = (): ReactElement => {
    const a = import.meta.env.VITE_REACT_APP_CLIENT_ID
    console.log(a);


    return (
        <>
            <section className="loading-body">
                <div className="loader">
                    <div className="inner-border"></div>
                </div>
            </section>
        </>

    );
};