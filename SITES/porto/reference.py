import requests

links = ['Home|https://portotheme.com/html/porto/8.1.0/index.html ', 'Landing Page|https://portotheme.com/html/porto/8.1.0/index.html ', 'Classic - Original|https://portotheme.com/html/porto/8.1.0/index-classic.html ', 'Classic - Color|https://portotheme.com/html/porto/8.1.0/index-classic-color.html ', 'Classic - Light|https://portotheme.com/html/porto/8.1.0/index-classic-light.html ', 'Classic - Video|https://portotheme.com/html/porto/8.1.0/index-classic-video.html ', 'Classic - Video - Light|https://portotheme.com/html/porto/8.1.0/index-classic-video-light.html ', 'Corporate - Version 1|https://portotheme.com/html/porto/8.1.0/index-corporate.html ', 'Corporate - Version 2|https://portotheme.com/html/porto/8.1.0/index-corporate-2.html ', 'Corporate - Version 3|https://portotheme.com/html/porto/8.1.0/index-corporate-3.html ', 'Corporate - Version 4|https://portotheme.com/html/porto/8.1.0/index-corporate-4.html ', 'Corporate - Version 5|https://portotheme.com/html/porto/8.1.0/index-corporate-5.html ', 'Corporate - Version 6|https://portotheme.com/html/porto/8.1.0/index-corporate-6.html ', 'Corporate - Version 7|https://portotheme.com/html/porto/8.1.0/index-corporate-7.html ', 'Corporate - Version 8|https://portotheme.com/html/porto/8.1.0/index-corporate-8.html ', 'Corporate - Version 9|https://portotheme.com/html/porto/8.1.0/index-corporate-9.html ', 'Corporate - Version 10|https://portotheme.com/html/porto/8.1.0/index-corporate-10.html ', 'Corporate - Version 11|https://portotheme.com/html/porto/8.1.0/index-corporate-11.html ', 'Corporate - Version 12|https://portotheme.com/html/porto/8.1.0/index-corporate-12.html ', 'Corporate - Version 13|https://portotheme.com/html/porto/8.1.0/index-corporate-13.html ', 'Corporate - Version 14|https://portotheme.com/html/porto/8.1.0/index-corporate-14.html ', 'Corporate - Version 15|https://portotheme.com/html/porto/8.1.0/index-corporate-15.html ', 'Corporate - Version 16|https://portotheme.com/html/porto/8.1.0/index-corporate-16.html ', 'Corporate - Version 17|https://portotheme.com/html/porto/8.1.0/index-corporate-17.html ', 'Corporate - Version 18|https://portotheme.com/html/porto/8.1.0/index-corporate-18.html ', 'Corporate - Version 19|https://portotheme.com/html/porto/8.1.0/index-corporate-19.html ', 'Corporate - Version 20|https://portotheme.com/html/porto/8.1.0/index-corporate-20.html ', 'Portfolio - Version 1|https://portotheme.com/html/porto/8.1.0/index-portfolio.html ', 'Portfolio - Version 2|https://portotheme.com/html/porto/8.1.0/index-portfolio-2.html ', 'Portfolio - Version 3|https://portotheme.com/html/porto/8.1.0/index-portfolio-3.html ', 'Portfolio - Version 4|https://portotheme.com/html/porto/8.1.0/index-portfolio-4.html ', 'Portfolio - Version 5|https://portotheme.com/html/porto/8.1.0/index-portfolio-5.html ', 'Blog - Version 1|https://portotheme.com/html/porto/8.1.0/index-blog.html ', 'Blog - Version 2|https://portotheme.com/html/porto/8.1.0/index-blog-2.html ', 'Blog - Version 3|https://portotheme.com/html/porto/8.1.0/index-blog-3.html ', 'Blog - Version 4|https://portotheme.com/html/porto/8.1.0/index-blog-4.html ', 'Blog - Version 5|https://portotheme.com/html/porto/8.1.0/index-blog-5.html ', 'One Page Original|https://portotheme.com/html/porto/8.1.0/index-one-page.html ', 'Elements|https://portotheme.com/html/porto/8.1.0/elements.html ', 'Accordions|https://portotheme.com/html/porto/8.1.0/elements-accordions.html ', 'Toggles|https://portotheme.com/html/porto/8.1.0/elements-toggles.html ', 'Tabs|https://portotheme.com/html/porto/8.1.0/elements-tabs.html ', 'Icons|https://portotheme.com/html/porto/8.1.0/elements-icons.html ', 'Icon Boxes|https://portotheme.com/html/porto/8.1.0/elements-icon-boxes.html ', 'Carousels|https://portotheme.com/html/porto/8.1.0/elements-carousels.html ', 'Modals|https://portotheme.com/html/porto/8.1.0/elements-modals.html ', 'Lightboxes|https://portotheme.com/html/porto/8.1.0/elements-lightboxes.html ', 'Word Rotator|https://portotheme.com/html/porto/8.1.0/elements-word-rotator.html ', 'Before / After|https://portotheme.com/html/porto/8.1.0/elements-before-after.html ', '360º Image Viewer|https://portotheme.com/html/porto/8.1.0/elements-360-image-viewer.html ', 'Buttons|https://portotheme.com/html/porto/8.1.0/elements-buttons.html ', 'Badges|https://portotheme.com/html/porto/8.1.0/elements-badges.html ', 'Lists|https://portotheme.com/html/porto/8.1.0/elements-lists.html ', 'Cards|https://portotheme.com/html/porto/8.1.0/elements-cards.html ', 'Image Gallery|https://portotheme.com/html/porto/8.1.0/elements-image-gallery.html ', 'Image Frames|https://portotheme.com/html/porto/8.1.0/elements-image-frames.html ', 'Image Hotspots|https://portotheme.com/html/porto/8.1.0/elements-image-hotspots.html ', 'Testimonials|https://portotheme.com/html/porto/8.1.0/elements-testimonials.html ', 'Blockquotes|https://portotheme.com/html/porto/8.1.0/elements-blockquotes.html ', 'Sticky Elements|https://portotheme.com/html/porto/8.1.0/elements-sticky-elements.html ', 'Shape Dividers|https://portotheme.com/html/porto/8.1.0/elements-shape-dividers.html ', 'Typography|https://portotheme.com/html/porto/8.1.0/elements-typography.html ', 'Call to Action|https://portotheme.com/html/porto/8.1.0/elements-call-to-action.html ', 'Pricing Tables|https://portotheme.com/html/porto/8.1.0/elements-pricing-tables.html ', 'Tables|https://portotheme.com/html/porto/8.1.0/elements-tables.html ', 'Progress Bars|https://portotheme.com/html/porto/8.1.0/elements-progressbars.html ', 'Process|https://portotheme.com/html/porto/8.1.0/elements-process.html ', 'Counters|https://portotheme.com/html/porto/8.1.0/elements-counters.html ', 'Countdowns|https://portotheme.com/html/porto/8.1.0/elements-countdowns.html ', 'Sections & Parallax|https://portotheme.com/html/porto/8.1.0/elements-sections-parallax.html ', 'Tooltips & Popovers|https://portotheme.com/html/porto/8.1.0/elements-tooltips-popovers.html ', 'Headings|https://portotheme.com/html/porto/8.1.0/elements-headings.html ', 'Dividers|https://portotheme.com/html/porto/8.1.0/elements-dividers.html ', 'Animations|https://portotheme.com/html/porto/8.1.0/elements-animations.html ', 'Medias|https://portotheme.com/html/porto/8.1.0/elements-medias.html ', 'Maps|https://portotheme.com/html/porto/8.1.0/elements-maps.html ', 'Arrows|https://portotheme.com/html/porto/8.1.0/elements-arrows.html ', 'Star Ratings|https://portotheme.com/html/porto/8.1.0/elements-star-ratings.html ', 'Alerts|https://portotheme.com/html/porto/8.1.0/elements-alerts.html ', 'Posts|https://portotheme.com/html/porto/8.1.0/elements-posts.html ', 'Forms|https://portotheme.com/html/porto/8.1.0/elements-forms-basic-contact.html ', 'Overview|https://portotheme.com/html/porto/8.1.0/feature-headers-overview.html ', 'Classic|https://portotheme.com/html/porto/8.1.0/feature-headers-classic.html ', 'Classic + Language Dropdown|https://portotheme.com/html/porto/8.1.0/feature-headers-classic-language-dropdown.html ', 'Classic + Big Logo|https://portotheme.com/html/porto/8.1.0/feature-headers-classic-big-logo.html ', 'Flat|https://portotheme.com/html/porto/8.1.0/feature-headers-flat.html ', 'Flat + Top Bar|https://portotheme.com/html/porto/8.1.0/feature-headers-flat-top-bar.html ', 'Flat + Top Bar + Top Border|https://portotheme.com/html/porto/8.1.0/feature-headers-flat-top-bar-top-borders.html ', 'Flat + Colored Top Bar|https://portotheme.com/html/porto/8.1.0/feature-headers-flat-colored-top-bar.html ', 'Flat + Borders|https://portotheme.com/html/porto/8.1.0/feature-headers-flat-borders.html ', 'Center|https://portotheme.com/html/porto/8.1.0/feature-headers-center.html ', 'Center + Double Navs|https://portotheme.com/html/porto/8.1.0/feature-headers-center-double-navs.html ', 'Center + Nav + Buttons|https://portotheme.com/html/porto/8.1.0/feature-headers-center-nav-buttons.html ', 'Center Below Slider|https://portotheme.com/html/porto/8.1.0/feature-headers-center-below-slider.html ', 'Floating Bar|https://portotheme.com/html/porto/8.1.0/feature-headers-floating-bar.html ', 'Floating Icons|https://portotheme.com/html/porto/8.1.0/feature-headers-floating-icons.html ', 'Below Slider|https://portotheme.com/html/porto/8.1.0/feature-headers-below-slider.html ', 'Full Video|https://portotheme.com/html/porto/8.1.0/feature-headers-full-video.html ', 'Narrow|https://portotheme.com/html/porto/8.1.0/feature-headers-narrow.html ', 'Sticky Shrink|https://portotheme.com/html/porto/8.1.0/feature-headers-sticky-shrink.html ', 'Sticky Static|https://portotheme.com/html/porto/8.1.0/feature-headers-sticky-static.html ', 'Sticky Change Logo|https://portotheme.com/html/porto/8.1.0/feature-headers-sticky-change-logo.html ', 'Sticky Reveal|https://portotheme.com/html/porto/8.1.0/feature-headers-sticky-reveal.html ', 'Transparent Light|https://portotheme.com/html/porto/8.1.0/feature-headers-transparent-light.html ', 'Transparent Dark|https://portotheme.com/html/porto/8.1.0/feature-headers-transparent-dark.html ', 'Transparent Light + Bottom Border|https://portotheme.com/html/porto/8.1.0/feature-headers-transparent-light-bottom-border.html ', 'Transparent Dark + Bottom Border|https://portotheme.com/html/porto/8.1.0/feature-headers-transparent-dark-bottom-border.html ', 'Transparent Bottom Slider|https://portotheme.com/html/porto/8.1.0/feature-headers-transparent-bottom-slider.html ', 'Semi Transparent Light|https://portotheme.com/html/porto/8.1.0/feature-headers-semi-transparent-light.html ', 'Semi Transparent Dark|https://portotheme.com/html/porto/8.1.0/feature-headers-semi-transparent-dark.html ', 'Semi Transparent Bottom Slider|https://portotheme.com/html/porto/8.1.0/feature-headers-semi-transparent-bottom-slider.html ', 'Semi Transparent + Top Bar + Borders|https://portotheme.com/html/porto/8.1.0/feature-headers-semi-transparent-top-bar-borders.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/feature-headers-full-width.html ', 'Full Width + Borders|https://portotheme.com/html/porto/8.1.0/feature-headers-full-width-borders.html ', 'Full Width Transparent Light|https://portotheme.com/html/porto/8.1.0/feature-headers-full-width-transparent-light.html ', 'Full Width Transparent Dark|https://portotheme.com/html/porto/8.1.0/feature-headers-full-width-transparent-dark.html ', 'Full Width Semi Transparent Light|https://portotheme.com/html/porto/8.1.0/feature-headers-full-width-semi-transparent-light.html ', 'Full Width Semi Transparent Dark|https://portotheme.com/html/porto/8.1.0/feature-headers-full-width-semi-transparent-dark.html ', 'Navbar|https://portotheme.com/html/porto/8.1.0/feature-headers-navbar.html ', 'Navbar Full|https://portotheme.com/html/porto/8.1.0/feature-headers-navbar-full.html ', 'Navbar Pills|https://portotheme.com/html/porto/8.1.0/feature-headers-navbar-pills.html ', 'Navbar Divisors|https://portotheme.com/html/porto/8.1.0/feature-headers-navbar-divisors.html ', 'Nav Bar + Icons + Search|https://portotheme.com/html/porto/8.1.0/feature-headers-navbar-icons-search.html ', 'Dropdown|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-left-dropdown.html ', 'Expand|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-left-expand.html ', 'Columns|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-left-columns.html ', 'Slide|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-left-slide.html ', 'Semi Transparent|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-left-semi-transparent.html ', 'Dark|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-left-dark.html ', 'Dropdown|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-right-dropdown.html ', 'Expand|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-right-expand.html ', 'Columns|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-right-columns.html ', 'Slide|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-right-slide.html ', 'Semi Transparent|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-right-semi-transparent.html ', 'Dark|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-right-dark.html ', 'Push|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-offcanvas-push.html ', 'Slide|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-offcanvas-slide.html ', 'Side Header Narrow Bar|https://portotheme.com/html/porto/8.1.0/feature-headers-side-header-narrow-bar.html ', 'Sign In / Sign Up|https://portotheme.com/html/porto/8.1.0/feature-headers-sign-in-sign-up.html ', 'Logged|https://portotheme.com/html/porto/8.1.0/feature-headers-logged.html ', 'Mini Cart|https://portotheme.com/html/porto/8.1.0/feature-headers-mini-cart.html ', 'Simple Input|https://portotheme.com/html/porto/8.1.0/feature-headers-search-simple-input.html ', 'Simple Input Reveal|https://portotheme.com/html/porto/8.1.0/feature-headers-search-simple-input-reveal.html ', 'Dropdown|https://portotheme.com/html/porto/8.1.0/feature-headers-search-dropdown.html ', 'Big Input Hidden|https://portotheme.com/html/porto/8.1.0/feature-headers-search-big-input-hidden.html ', 'Full Screen|https://portotheme.com/html/porto/8.1.0/feature-headers-search-full-screen.html ', 'Big Icon|https://portotheme.com/html/porto/8.1.0/feature-headers-extra-big-icon.html ', 'Big Icons Top|https://portotheme.com/html/porto/8.1.0/feature-headers-extra-big-icons-top.html ', 'Button|https://portotheme.com/html/porto/8.1.0/feature-headers-extra-button.html ', 'Background Color|https://portotheme.com/html/porto/8.1.0/feature-headers-extra-background-color.html ', 'Pills|https://portotheme.com/html/porto/8.1.0/feature-navigations-pills.html ', 'Pills + Arrows|https://portotheme.com/html/porto/8.1.0/feature-navigations-pills-arrows.html ', 'Pills Dark Text|https://portotheme.com/html/porto/8.1.0/feature-navigations-pills-dark-text.html ', 'Pills Color Dropdown|https://portotheme.com/html/porto/8.1.0/feature-navigations-pills-color-dropdown.html ', 'Pills Square|https://portotheme.com/html/porto/8.1.0/feature-navigations-pills-square.html ', 'Pills Rounded|https://portotheme.com/html/porto/8.1.0/feature-navigations-pills-rounded.html ', 'Stripe|https://portotheme.com/html/porto/8.1.0/feature-navigations-stripe.html ', 'Stripe Dark Text|https://portotheme.com/html/porto/8.1.0/feature-navigations-stripe-dark-text.html ', 'Stripe Color Dropdown|https://portotheme.com/html/porto/8.1.0/feature-navigations-stripe-color-dropdown.html ', 'Top Line|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-top-line.html ', 'Top Line Animated|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-top-line-animated.html ', 'Top Line Color Dropdown|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-top-line-color-dropdown.html ', 'Bottom Line|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-bottom-line.html ', 'Bottom Line Animated|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-bottom-line-animated.html ', 'Slide|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-slide.html ', 'Sub Title|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-sub-title.html ', 'Line Under Text|https://portotheme.com/html/porto/8.1.0/feature-navigations-hover-line-under-text.html ', 'Dropdown|https://portotheme.com/html/porto/8.1.0/feature-navigations-vertical-dropdown.html ', 'Expand|https://portotheme.com/html/porto/8.1.0/feature-navigations-vertical-expand.html ', 'Columns|https://portotheme.com/html/porto/8.1.0/feature-navigations-vertical-columns.html ', 'Slide|https://portotheme.com/html/porto/8.1.0/feature-navigations-vertical-slide.html ', 'Sidebar|https://portotheme.com/html/porto/8.1.0/feature-navigations-hamburguer-sidebar.html ', 'Overlay|https://portotheme.com/html/porto/8.1.0/feature-navigations-hamburguer-overlay.html ', 'Dark|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-dark.html ', 'Light|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-light.html ', 'Colors|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-colors.html ', 'Top Line|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-top-line.html ', 'Square|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-square.html ', 'Arrow Dropdown|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-arrow.html ', 'Arrow Center Dropdown|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-arrow-center.html ', 'Modern Light|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-modern-light.html ', 'Modern Dark|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-modern-dark.html ', 'No Effect|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-effect-no-effect.html ', 'Opacity|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-effect-opacity.html ', 'Move To Top|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-effect-move-to-top.html ', 'Move To Bottom|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-effect-move-to-bottom.html ', 'Move To Right|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-effect-move-to-right.html ', 'Move To Left|https://portotheme.com/html/porto/8.1.0/feature-navigations-dropdowns-effect-move-to-left.html ', 'Small|https://portotheme.com/html/porto/8.1.0/feature-navigations-font-small.html ', 'Medium|https://portotheme.com/html/porto/8.1.0/feature-navigations-font-medium.html ', 'Large|https://portotheme.com/html/porto/8.1.0/feature-navigations-font-large.html ', 'Alternative|https://portotheme.com/html/porto/8.1.0/feature-navigations-font-alternative.html ', 'Icons|https://portotheme.com/html/porto/8.1.0/feature-navigations-icons.html ', 'Float Icons|https://portotheme.com/html/porto/8.1.0/feature-navigations-icons-float-icons.html ', 'Sub Title|https://portotheme.com/html/porto/8.1.0/feature-navigations-sub-title.html ', 'Divisors|https://portotheme.com/html/porto/8.1.0/feature-navigations-divisors.html ', 'Logo Between|https://portotheme.com/html/porto/8.1.0/feature-navigations-logo-between.html ', 'One Page Nav|https://portotheme.com/html/porto/8.1.0/feature-navigations-one-page.html ', 'Click To Open|https://portotheme.com/html/porto/8.1.0/feature-navigations-click-to-open.html ', 'Overview|https://portotheme.com/html/porto/8.1.0/feature-page-headers-overview.html ', 'Small|https://portotheme.com/html/porto/8.1.0/feature-page-headers-classic-small.html ', 'Medium|https://portotheme.com/html/porto/8.1.0/feature-page-headers-classic-medium.html ', 'Large|https://portotheme.com/html/porto/8.1.0/feature-page-headers-classic-large.html ', 'Small|https://portotheme.com/html/porto/8.1.0/feature-page-headers-modern-small.html ', 'Medium|https://portotheme.com/html/porto/8.1.0/feature-page-headers-modern-medium.html ', 'Large|https://portotheme.com/html/porto/8.1.0/feature-page-headers-modern-large.html ', 'Primary|https://portotheme.com/html/porto/8.1.0/feature-page-headers-colors-primary.html ', 'Secondary|https://portotheme.com/html/porto/8.1.0/feature-page-headers-colors-secondary.html ', 'Tertiary|https://portotheme.com/html/porto/8.1.0/feature-page-headers-colors-tertiary.html ', 'Quaternary|https://portotheme.com/html/porto/8.1.0/feature-page-headers-colors-quaternary.html ', 'Light|https://portotheme.com/html/porto/8.1.0/feature-page-headers-colors-light.html ', 'Dark|https://portotheme.com/html/porto/8.1.0/feature-page-headers-colors-dark.html ', 'Small|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-left-small.html ', 'Medium|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-left-medium.html ', 'Large|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-left-large.html ', 'Small|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-right-small.html ', 'Medium|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-right-medium.html ', 'Large|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-right-large.html ', 'Small|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-center-small.html ', 'Medium|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-center-medium.html ', 'Large|https://portotheme.com/html/porto/8.1.0/feature-page-headers-title-position-center-large.html ', 'Fixed|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-fixed.html ', 'Parallax|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-parallax.html ', 'Video|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-video.html ', 'Transparent Header|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-transparent-header.html ', 'Pattern|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-pattern.html ', 'Overlay|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-overlay.html ', 'Clean (No Background)|https://portotheme.com/html/porto/8.1.0/feature-page-headers-background-clean.html ', 'Outside|https://portotheme.com/html/porto/8.1.0/feature-page-headers-extra-breadcrumb-outside.html ', 'Dark|https://portotheme.com/html/porto/8.1.0/feature-page-headers-extra-breadcrumb-dark.html ', 'Scroll to Content|https://portotheme.com/html/porto/8.1.0/feature-page-headers-extra-scroll-to-content.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/feature-page-headers-extra-full-width.html ', 'Overview|https://portotheme.com/html/porto/8.1.0/feature-footers-overview.html ', 'Forms Basic|https://portotheme.com/html/porto/8.1.0/feature-admin-forms-basic.html ', 'Forms Advanced|https://portotheme.com/html/porto/8.1.0/feature-admin-forms-advanced.html ', 'Forms Wizard|https://portotheme.com/html/porto/8.1.0/feature-admin-forms-wizard.html ', 'Code Editor|https://portotheme.com/html/porto/8.1.0/feature-admin-forms-code-editor.html ', 'Tables Advanced|https://portotheme.com/html/porto/8.1.0/feature-admin-tables-advanced.html ', 'Tables Responsive|https://portotheme.com/html/porto/8.1.0/feature-admin-tables-responsive.html ', 'Tables Editable|https://portotheme.com/html/porto/8.1.0/feature-admin-tables-editable.html ', 'Tables Ajax|https://portotheme.com/html/porto/8.1.0/feature-admin-tables-ajax.html ', 'Charts|https://portotheme.com/html/porto/8.1.0/feature-admin-charts.html ', 'Revolution Slider|https://portotheme.com/html/porto/8.1.0/index-classic.html ', 'Owl Slider|https://portotheme.com/html/porto/8.1.0/index-slider-owl.html ', 'Boxed|https://portotheme.com/html/porto/8.1.0/feature-layout-boxed.html ', 'Dark|https://portotheme.com/html/porto/8.1.0/feature-layout-dark.html ', 'RTL|https://portotheme.com/html/porto/8.1.0/feature-layout-rtl.html ', 'Grid System|https://portotheme.com/html/porto/8.1.0/feature-grid-system.html ', 'Page Loading|https://portotheme.com/html/porto/8.1.0/feature-page-loading.html ', 'Page Transition|https://portotheme.com/html/porto/8.1.0/feature-page-transition.html ', 'Lazy Load|https://portotheme.com/html/porto/8.1.0/feature-lazy-load.html ', 'Side Panel|https://portotheme.com/html/porto/8.1.0/feature-side-panel.html ', 'Contact Us - Advanced|https://portotheme.com/html/porto/8.1.0/contact-us-advanced.php ', 'Contact Us - Basic|https://portotheme.com/html/porto/8.1.0/contact-us.html ', 'Contact Us - Recaptcha|https://portotheme.com/html/porto/8.1.0/contact-us-recaptcha.html ', 'About Us - Advanced|https://portotheme.com/html/porto/8.1.0/about-us-advanced.html ', 'About Us - Basic|https://portotheme.com/html/porto/8.1.0/about-us.html ', 'About Me|https://portotheme.com/html/porto/8.1.0/about-me.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/page-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/page-left-sidebar.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/page-right-sidebar.html ', 'Left and Right Sidebars|https://portotheme.com/html/porto/8.1.0/page-left-and-right-sidebars.html ', 'Sticky Sidebar|https://portotheme.com/html/porto/8.1.0/page-sticky-sidebar.html ', 'Secondary Navbar|https://portotheme.com/html/porto/8.1.0/page-secondary-navbar.html ', '404 Error|https://portotheme.com/html/porto/8.1.0/page-404.html ', '500 Error|https://portotheme.com/html/porto/8.1.0/page-500.html ', 'Coming Soon|https://portotheme.com/html/porto/8.1.0/page-coming-soon.html ', 'Maintenance Mode|https://portotheme.com/html/porto/8.1.0/page-maintenance-mode.html ', 'Search Results|https://portotheme.com/html/porto/8.1.0/page-search-results.html ', 'Sitemap|https://portotheme.com/html/porto/8.1.0/sitemap.html ', 'Team - Advanced|https://portotheme.com/html/porto/8.1.0/page-team-advanced.html ', 'Team - Basic|https://portotheme.com/html/porto/8.1.0/page-team.html ', 'Services - Version 1|https://portotheme.com/html/porto/8.1.0/page-services.html ', 'Services - Version 2|https://portotheme.com/html/porto/8.1.0/page-services-2.html ', 'Services - Version 3|https://portotheme.com/html/porto/8.1.0/page-services-3.html ', 'Custom Header|https://portotheme.com/html/porto/8.1.0/page-custom-header.html ', 'Careers|https://portotheme.com/html/porto/8.1.0/page-careers.html ', 'FAQ|https://portotheme.com/html/porto/8.1.0/page-faq.html ', 'Login / Register|https://portotheme.com/html/porto/8.1.0/page-login.html ', 'User Profile|https://portotheme.com/html/porto/8.1.0/page-user-profile.html ', 'Wide Slider|https://portotheme.com/html/porto/8.1.0/portfolio-single-wide-slider.html ', 'Small Slider|https://portotheme.com/html/porto/8.1.0/portfolio-single-small-slider.html ', 'Full Width Slider|https://portotheme.com/html/porto/8.1.0/portfolio-single-full-width-slider.html ', 'Gallery|https://portotheme.com/html/porto/8.1.0/portfolio-single-gallery.html ', 'Carousel|https://portotheme.com/html/porto/8.1.0/portfolio-single-carousel.html ', 'Medias|https://portotheme.com/html/porto/8.1.0/portfolio-single-medias.html ', 'Full Width Video|https://portotheme.com/html/porto/8.1.0/portfolio-single-full-width-video.html ', 'Masonry Images|https://portotheme.com/html/porto/8.1.0/portfolio-single-masonry-images.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/portfolio-single-left-sidebar.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/portfolio-single-right-sidebar.html ', 'Left and Right Sidebars|https://portotheme.com/html/porto/8.1.0/portfolio-single-left-and-right-sidebars.html ', 'Sticky Sidebar|https://portotheme.com/html/porto/8.1.0/portfolio-single-sticky-sidebar.html ', 'Extended|https://portotheme.com/html/porto/8.1.0/portfolio-single-extended.html ', '1 Column|https://portotheme.com/html/porto/8.1.0/portfolio-grid-1-column.html ', '2 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-grid-2-columns.html ', '3 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-grid-3-columns.html ', '4 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-grid-4-columns.html ', '5 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-grid-5-columns.html ', '6 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-grid-6-columns.html ', 'No Margins|https://portotheme.com/html/porto/8.1.0/portfolio-grid-no-margins.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/portfolio-grid-full-width.html ', 'Full Width No Margins|https://portotheme.com/html/porto/8.1.0/portfolio-grid-full-width-no-margins.html ', 'Title and Description|https://portotheme.com/html/porto/8.1.0/portfolio-grid-1-column-title-and-description.html ', '2 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-2-columns.html ', '3 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-3-columns.html ', '4 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-4-columns.html ', '5 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-5-columns.html ', '6 Columns|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-6-columns.html ', 'No Margins|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-no-margins.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/portfolio-masonry-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/portfolio-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/portfolio-sidebar-right.html ', 'Left and Right Sidebars|https://portotheme.com/html/porto/8.1.0/portfolio-sidebar-left-and-right.html ', 'Sticky Sidebar|https://portotheme.com/html/porto/8.1.0/portfolio-sidebar-sticky.html ', 'Ajax on Page|https://portotheme.com/html/porto/8.1.0/portfolio-ajax-page.html ', 'Ajax on Modal|https://portotheme.com/html/porto/8.1.0/portfolio-ajax-modal.html ', 'Timeline|https://portotheme.com/html/porto/8.1.0/portfolio-extra-timeline.html ', 'Lightbox|https://portotheme.com/html/porto/8.1.0/portfolio-extra-lightbox.html ', 'Load More|https://portotheme.com/html/porto/8.1.0/portfolio-extra-load-more.html ', 'Infinite Scroll|https://portotheme.com/html/porto/8.1.0/portfolio-extra-infinite-scroll.html ', 'Pagination|https://portotheme.com/html/porto/8.1.0/portfolio-extra-pagination.html ', 'Combination Filters|https://portotheme.com/html/porto/8.1.0/portfolio-extra-combination-filters.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/blog-large-image-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/blog-large-image-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-large-image-sidebar-right.html ', 'Left and Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-large-image-sidebar-left-and-right.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/blog-medium-image-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-medium-image-sidebar-right.html ', '4 Columns|https://portotheme.com/html/porto/8.1.0/blog-grid-4-columns.html ', '3 Columns|https://portotheme.com/html/porto/8.1.0/blog-grid-3-columns.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/blog-grid-full-width.html ', 'No Margins|https://portotheme.com/html/porto/8.1.0/blog-grid-no-margins.html ', 'No Margins Full Width|https://portotheme.com/html/porto/8.1.0/blog-grid-no-margins-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/blog-grid-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-grid-sidebar-right.html ', 'Left and Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-grid-sidebar-left-and-right.html ', '4 Columns|https://portotheme.com/html/porto/8.1.0/blog-masonry-4-columns.html ', '3 Columns|https://portotheme.com/html/porto/8.1.0/blog-masonry-3-columns.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/blog-masonry-full-width.html ', 'No Margins|https://portotheme.com/html/porto/8.1.0/blog-masonry-no-margins.html ', 'No Margins Full Width|https://portotheme.com/html/porto/8.1.0/blog-masonry-no-margins-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/blog-masonry-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-masonry-sidebar-right.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/blog-timeline.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/blog-timeline-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-timeline-sidebar-right.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/blog-post.html ', 'Slider Gallery|https://portotheme.com/html/porto/8.1.0/blog-post-slider-gallery.html ', 'Image Gallery|https://portotheme.com/html/porto/8.1.0/blog-post-image-gallery.html ', 'Embedded Video|https://portotheme.com/html/porto/8.1.0/blog-post-embedded-video.html ', 'HTML5 Video|https://portotheme.com/html/porto/8.1.0/blog-post-html5-video.html ', 'Blockquote|https://portotheme.com/html/porto/8.1.0/blog-post-blockquote.html ', 'Link|https://portotheme.com/html/porto/8.1.0/blog-post-link.html ', 'Embedded Audio|https://portotheme.com/html/porto/8.1.0/blog-post-embedded-audio.html ', 'Small Image|https://portotheme.com/html/porto/8.1.0/blog-post-small-image.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/blog-post-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-post-sidebar-right.html ', 'Left and Right Sidebar|https://portotheme.com/html/porto/8.1.0/blog-post-sidebar-left-and-right.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/shop-product-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/shop-product-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-product-sidebar-right.html ', 'Left and Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-product-sidebar-left-and-right.html ', '4 Columns|https://portotheme.com/html/porto/8.1.0/shop-4-columns.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/shop-3-columns-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/shop-3-columns-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-3-columns-sidebar-right.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/shop-2-columns-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/shop-2-columns-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-2-columns-sidebar-right.html ', 'Left and Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-2-columns-sidebar-left-and-right.html ', 'Full Width|https://portotheme.com/html/porto/8.1.0/shop-1-column-full-width.html ', 'Left Sidebar|https://portotheme.com/html/porto/8.1.0/shop-1-column-sidebar-left.html ', 'Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-1-column-sidebar-right.html ', 'Left and Right Sidebar|https://portotheme.com/html/porto/8.1.0/shop-1-column-sidebar-left-and-right.html ', 'Cart|https://portotheme.com/html/porto/8.1.0/shop-cart.html ', 'Login|https://portotheme.com/html/porto/8.1.0/shop-login.html ', 'Checkout|https://portotheme.com/html/porto/8.1.0/shop-checkout.html ', 'Order Complete|https://portotheme.com/html/porto/8.1.0/shop-order-complete.html']


def req(url):
    z = 0
    while True:
        z += 1
        print(z, url)
        if z > 10:
            break
        try:
            r = requests.get(url, timeout = 5)
            return r.text
        except Exception as e:
            print(e)

def get_links():
    for i, link in enumerate(links):
        url = link.split('|')[1].strip()
        text = req(url)
        if not text:
            continue
        fname = url.split('/')[-1].strip()
        with open('/home/jocker/Downloads/porto/%s' % fname, 'w+', encoding='utf-8') as f:
            f.write(text)
            print(fname, i, '/', len(links))
get_links()