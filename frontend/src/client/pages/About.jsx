import React from "react";

import CommonSection from "@client/components/UI/CommonSection";
import Helmet from "@client/components/Helmet/Helmet";
import AboutSection from "@client/components/UI/AboutSection";
import { Container, Row, Col } from "reactstrap";
import driveImg from "@assets/all-images/upward.png";
import OurMembers from "@client/components/UI/OurMembers";
import "@client/styles/about.css";
import OurFeature from "@client/components/UI/OurFeature";

// window.location.reload()
const About = () => {
  return (
    <Helmet title="About">
      <CommonSection title="About Us" />
      <AboutSection aboutClass="aboutPage" />

      <section className="about__page-section" style={{backgroundColor:'#f7fbf1'}}>
        <Container>
          <Row>
            <Col lg="6" md="6" sm="12">
              <div className="about__page-img">
                <img src={driveImg} alt="" className="w-100 rounded-3" style={{height:'500px'}} />
              </div>
            </Col>

            <Col lg="6" md="6" sm="12">
              <div className="about__page-content">
                <h2 className="section__title">
                Our mission is to help you better understand ESGs and guide you toward achieving the SDGs.
                </h2>

                <p className="section__description">
                In Vietnam, many businesses claim to be sustainable without adhering to any formal evaluation frameworks. Assessing genuine sustainability is complex, requiring years of operational data and extensive metric analysis, which poses challenges for government bodies and non-profits seeking accurate evaluations. Meanwhile, many small and medium-sized enterprises (SMEs) in Vietnam aim to align with the SDGs. Beyond environmental protection, they can benefit from tax reductions on sustainability initiatives and access significant funding opportunities. Our platform simplifies sustainability assessments, offering transparent insights into a business’s ESG performance. This saves time for non-profits and government organizations while also guiding SMEs toward sustainable practices through tailored consultation.
                </p>

                <p className="section__description">
                Our customers come from all around the world. The value we deliver to your hands is our mission. Customer satisfaction is what our company strives for.
                </p>

                <div className=" d-flex align-items-center gap-3 mt-4">
                  <span className="fs-4">
                    <i className="ri-phone-line"></i>
                  </span>

                  <div>
                    <h6 className="section__subtitle">Need Any Help?</h6>
                    <h4>+0938922810</h4>
                  </div>
                </div>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      
      <OurFeature/>

      {/* <BecomeOurCustomer /> */}

      <section>
        <Container>
          <Row>
            <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">Experts</h6>
              <h2 className="section__title">Our Members</h2>
            </Col>
            <OurMembers />
          </Row>
        </Container>
      </section>
    </Helmet>
  );
};

export default About;
