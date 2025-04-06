import React from "react";
import { Container, Row, Col } from "reactstrap";
import "@client/styles/about-section.css";
import aboutImg from "/media/bitcoin.png";

const AboutSection = ({ aboutClass }) => {
  return (
    <section
      className="about__section"
      style={
        aboutClass === "aboutPage"
          ? { marginTop: "0px", backgroundColor:'#f7fbf1' }
          : { marginTop: "0px", backgroundColor:'#f7fbf1' }
      }
    >
      <Container>
        <Row>
          <Col lg="6" md="6">
            <div className="about__section-content">
              <h4 className="section__subtitle">About Us</h4>
              <h2 className="section__title">Welcome to Ecoscore AI</h2>
              <p className="section__description">
              Ecoscore AI is a platform that quickly and accurately evaluates ESG metrics for businesses based on a wide range of verified and reliable data sources. The platform enables government organizations, non-profits, users, and even the businesses themselves to effectively assess ESG scores, precisely track activities related to sustainable consumption, and detect fraudulent behaviors in the pursuit of SDG goals.
              </p>

              <div className="about__section-item d-flex align-items-center">
                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i> Use API to get data from Vnstock markets 
                </p>

                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i> Visualize with chart and statistic easily
                </p>
              </div>

              <div className="about__section-item d-flex align-items-center">
                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i> Use Machine Learning for automatic task
                </p>

                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i>Build powerful chatbot system apply modern technology
                </p>
              </div>
            </div>
          </Col>

          <Col lg="6" md="6">
            <div className="about__img">
              <img src={aboutImg} alt="" className="w-100" />
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default AboutSection;
