import "./Footer.css";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          {/* About Section */}
          <div className="footer-section">
            <h4>About PriceCompare</h4>
            <p>
              Find and compare prices of electronic products across multiple online stores.
              Save time and money with our intelligent price comparison platform.
            </p>
          </div>

          {/* Quick Links */}
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#products">Products</a></li>
              <li><a href="#about">About Us</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          {/* Categories */}
          <div className="footer-section">
            <h4>Categories</h4>
            <ul>
              <li><a href="#phones">Phones</a></li>
              <li><a href="#laptops">Laptops</a></li>
              <li><a href="#tablets">Tablets</a></li>
              <li><a href="#smartwatches">Smartwatches</a></li>
            </ul>
          </div>

          {/* Support */}
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li><a href="#faq">FAQ</a></li>
              <li><a href="#privacy">Privacy Policy</a></li>
              <li><a href="#terms">Terms of Service</a></li>
              <li><a href="#contact">Contact Support</a></li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <p>&copy; {currentYear} PriceCompare. All rights reserved.</p>
          <p>Built with ❤️ for smart shoppers</p>
        </div>
      </div>
    </footer>
  );
}
