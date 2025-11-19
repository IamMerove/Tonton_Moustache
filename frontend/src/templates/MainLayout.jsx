import React from "react";
import AsideMenu from "./AsideMenu";

function MainLayout({ children }) {
  return (
    <div style={{ display: "flex" }}>
      <AsideMenu />
      <div style={{ flex: 1, padding: "20px" }}>
        {children}
      </div>
    </div>
  );
}

export default MainLayout;
