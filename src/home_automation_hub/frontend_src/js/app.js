import $ from "jquery"
import "@coreui/coreui"
import css from "../css/app.scss"
import "bootstrap"

import "./websockets.js"

// BEGIN fontawesome setup
import fontawesome from "@fortawesome/fontawesome";
import fa_regular from "@fortawesome/fontawesome-free-regular";
import fa_solid from "@fortawesome/fontawesome-free-solid";
import fa_brands from "@fortawesome/fontawesome-free-brands";

fontawesome.library.add(fa_regular);
fontawesome.library.add(fa_solid);
fontawesome.library.add(fa_brands);
// END fontawesome setup

window.jQuery = $ // Make jQuery accessable globally so that modules can use it
