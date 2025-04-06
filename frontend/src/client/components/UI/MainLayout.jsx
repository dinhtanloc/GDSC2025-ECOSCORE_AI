import { Outlet } from 'react-router-dom';

const MainLayout = () => {
  return (
    <div style={{ backgroundColor: '#f7fbf1' }}>
      <Outlet />
    </div>
  );
};

export default MainLayout;
