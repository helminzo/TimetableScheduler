import React from "react";
import "./Header.css";
import SearchIcon from '@mui/icons-material/Search';
function Header() {
  return (
    <div className="header">
      <img
        className="header_logo"
        src="https://learntolead.in/wp-content/uploads/2020/01/sat.png"
      />

      <div className="header_search">
        <input className="header_searchInput" type="text" />
        <SearchIcon className="header_searchIcon" />
      </div>

      <div className="header_nav">
        <div className="header_option">
          <span className="header_optionLineOne">Pooi</span>
          <span className="header_optionLineTwo">Sign In</span>
        </div>

        <div className="header_option">
          <span className="header_optionLineOne">complaint</span>
          <span className="header_optionLineTwo">Contact</span>
        </div>

        <div className="header_option">
          <span className="header_optionLineOne">Become our</span>
          <span className="header_optionLineTwo">Premium Member</span>
        </div>

      </div>
    </div>
  );
}

export default Header;
