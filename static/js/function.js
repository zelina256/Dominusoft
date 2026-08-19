// -------NAVBAR-------
$(document).ready(function () {
  if ($(window).width() <= 992) {
    $(".dropdown ul").removeClass("drop_nav");
  }
});
$(document).ready(function () {
  $(".navbar-toggler").on("click", function () {
    $(".navbar-toggler .line").css({ background: "#acacac", border: "none" });
  });
});
$(document).ready(function () {
  if ($(window).width() >= 992) {
    $(
      ".drop_traj a.dropdown-toggle, .drop_apliko  a.dropdown-toggle"
    ).removeAttr("data-bs-toggle");
  }
  // FAQ
  $(".accordion-button:first").removeClass("collapsed");
});
// Dropdown hover
$(document).ready(function () {
  $("#home_index .navbar .drop_traj, #home_index .navbar .drop_apliko").on({
    mouseover: function () {
      $("#home .bread_crumb").css("background-color", "#31344b");
    },
    mouseleave: function () {
      $("#home .bread_crumb").css("background-color", "#e6e7ee");
    },
  });
});
// Search
$(document).ready(function () {
  $(".dropdown_search").on({
    click: function () {
      $("#home .bread_crumb").css("background-color", "#31344b");
    },
    submit: function () {
      $("#home .bread_crumb").css("background-color", "#e6e7ee");
    },
  });
});
// bread_crumb hover
$(document).ready(function () {
  $(".drop_traj, .drop_apliko").on({
    mouseover: function () {
      $(".bread_crumb .row").hide();
    },
    mouseleave: function () {
      $(".bread_crumb .row").show();
    },
  });
});
// ------Text size
// Trajnimet kryefaqja
$(document).ready(function () {
  if ($(window).width() >= 1400) {
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength > 215) {
        el.css("font-size", "0.9895rem");
      }
    });
  }
  if ($(window).width() <= 1399) {
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength < 180) {
        el.css("font-size", "1.0489rem");
      }
      $(".titull_trajnim").each(function () {
        var el = $(this);
        var textLength = el.html().length;
        if (textLength > 18) {
          el.css("font-size", "1.45rem");
        }
      });
    });
  }
  if ($(window).width() <= 1025) {
    $(".titull_trajnim").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength <= 25) {
        el.css("font-size", "1.8rem");
      }
    });
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength >= 200 && textLength <= 210) {
        el.css("font-size", "0.995rem");
      }
    });
  }
  if ($(window).width() >= 922 && $(window).width() <= 1024) {
    $(".titull_trajnim").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength < 50) {
        el.css("font-size", "1.5rem");
      }
    });
    $(".titull_trajnim").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength <= 35) {
        el.css("font-size", "1.9rem");
      }
    });
  }
  if ($(window).width() <= 922) {
    $(".titull_trajnim").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength > 18) {
        el.css("font-size", "1.7rem");
      }
    });
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength < 180) {
        el.css("font-size", "1.2rem");
      }
    });
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength < 190) {
        el.css("font-size", "1.0489rem");
      }
    });
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength > 200) {
        el.css("font-size", "1.088rem");
      }
    });
  }
  if ($(window).width() >= 768 && $(window).width() <= 992) {
    $(".text_trajnime").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength < 180) {
        el.css("font-size", "1.19rem");
      }
    });
    $(".titull_trajnim").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength <= 50) {
        el.css("font-size", "1.8rem");
      }
    });
  }
});
// Evente kryefaqja
$(document).ready(function () {
  $(".aktivitet p.h3, .calendar_train p.h3").each(function () {
    var el = $(this);
    var textLength = el.html().length;
    if (textLength > 12) {
      el.css("font-size", "1.1rem");
    }
  });
});
//bread crumb
$(document).ready(function () {
  if ($(window).width() <= 500) {
    $("li.breadcrumb-item").each(function () {
      var el = $(this);
      var textLength = el.html().length;
      if (textLength >= 4) {
        el.css("font-size", "0.85rem");
      }
    });
  }
});
// Counter
$(document).ready(function () {
  $({ countNum: $(".code").html() }).animate(
    // ndryshimi i numrit
    { countNum: 5900 },
    {
      duration: 8000,
      easing: "linear",
      step: function () {
        $(".code").html(Math.floor(this.countNum) + "+");
      },
      complete: function () {
        $(".code").html(this.countNum + "+");
      },
    }
  );
});
// ==== Carousel ====
// owl Testimonial
$(document).ready(function () {
  var owl = $(".testimonial");
  owl.owlCarousel({
    dotsEach: true,
    loop: true,
    nav: true,
    margin: 20,
    autoplay: true,
    autoplayTimeout: 5000,
    responsive: {
      0: {
        items: 1,
      },
    },
  });
  owl.on(".owl-stage", function (e) {
    if (e.deltaY > 0) {
      owl.trigger("next.owl");
    } else {
      owl.trigger("prev.owl");
    }
    e.preventDefault();
  });
});
// owl event
$(document).ready(function () {
  var owl = $(".event_carousel");
  owl.owlCarousel({
    items: 11,
    dotsEach: true,
    loop: true,
    nav: true,
    margin: 20,
    autoplay: true,
    autoplayTimeout: 5000,
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 2,
      },
      960: {
        items: 3,
      },
      1400: {
        items: 4,
      },
    },
  });
  owl.on(".owl-stage", function (e) {
    if (e.deltaY > 0) {
      owl.trigger("next.owl");
    } else {
      owl.trigger("prev.owl");
    }
    e.preventDefault();
  });
});
// owl partners
$(document).ready(function () {
  var owl = $(".partner");
  owl.owlCarousel({
    // items: 4,
    dotsEach: false,
    loop: true,
    nav: false,
    margin: 20,
    autoplay: true,
    autoplayTimeout: 5000,
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 3,
      },
      960: {
        items: 3,
      },
    },
  });
  owl.on(".owl-stage", function (e) {
    if (e.deltaY > 0) {
      owl.trigger("next.owl");
    } else {
      owl.trigger("prev.owl");
    }
    e.preventDefault();
  });
});
// kategori trajnime:
$(document).ready(function () {
  var owl = $(".kategori_trajnime");
  owl.owlCarousel({
    dotsEach: false,
    loop: true,
    nav: true,
    navText: ["", "<i class='fas fa-chevron-right' aria-hidden='true'></i>"],
    margin: 20,
    autoplay: true,
    autoplayTimeout: 5000,
    smartSpeed: 650,
    responsive: {
      0: {
        items: 1,
        stagePadding: 0,
      },
      600: {
        items: 2,
        stagePadding: 16,
      },
      960: {
        items: 3,
        // stagePadding: 72,
      },
    },
  });
  owl.on(".owl-stage", function (e) {
    if (e.deltaY > 0) {
      owl.trigger("next.owl");
    } else {
      owl.trigger("prev.owl");
    }
    e.preventDefault();
  });
});
// ==== Hover gif ====
// Pro_Kursant
$(document).ready(function () {
  $(".kursant_card, .internship_card").on({
    mouseover: function () {
      $(".kursant_img, .internship_img").hide();
      $(".kursant_gif, .internship_gif").show();
    },
    mouseleave: function () {
      $(".kursant_img, .internship_img").show();
      $(".kursant_gif, .internship_gif").hide();
    },
  });
});
// Internship
$(document).ready(function () {
  $(".internship_card").on({
    mouseover: function () {
      $(".internship_img").hide();
      $(".internship_gif").show();
    },
    mouseleave: function () {
      $(".internship_img").show();
      $(".internship_gif").hide();
    },
  });
});
// Viti tek copy right
$(document).ready(function () {
  $(".age").text(new Date().getFullYear() - 2014);
});
var legacyYear = document.getElementById("year");
if (legacyYear) {
  legacyYear.innerHTML = new Date().getFullYear();
}
