# Aiqube School Management System - Frontend

A modern, responsive React 18+ frontend for the Aiqube School Management System with Material-UI 5+ design and comprehensive features.

## 🚀 Features

### Core Features
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Material-UI 5+**: Modern, accessible, and customizable UI components
- **React Router v6**: Client-side routing with protected routes
- **React Query**: Efficient data fetching and caching
- **Form Validation**: React Hook Form with Yup validation
- **Authentication**: JWT-based authentication with role-based access control

### School Management Features
- **Dashboard**: Real-time statistics, charts, and quick actions
- **Student Management**: CRUD operations, profiles, and academic records
- **Teacher Management**: Staff profiles, assignments, and performance tracking
- **Attendance System**: Digital attendance tracking with reports
- **Fee Management**: Payment tracking, invoices, and financial reports
- **LMS Integration**: Course management, assignments, and learning materials

### AI-Powered Features
- **AI Assistant**: Intelligent doubt-solving and tutoring
- **Conversation History**: Track AI interactions and learning progress
- **Knowledge Base**: Subject-specific AI tutors and resources
- **Real-time Chat**: Interactive AI conversations

### Advanced Features
- **Blockchain Certificates**: Secure, tamper-proof digital credentials
- **AR/VR Content**: Virtual labs, simulations, and educational content
- **IoT Dashboard**: Smart campus monitoring and environmental control
- **Gamification**: Achievement badges, points, and leaderboards
- **Advanced Analytics**: Predictive models and behavioral analytics
- **Smart Scheduling**: AI-driven schedule optimization
- **Voice Assistant**: Natural language processing and voice commands
- **Biometric Attendance**: Multi-modal biometric authentication
- **Smart Classrooms**: Automated classroom management systems

## 🛠️ Technology Stack

- **React 18+**: Latest React with hooks and concurrent features
- **Material-UI 5+**: Modern component library with theming
- **React Router v6**: Client-side routing
- **React Query**: Data fetching and state management
- **React Hook Form**: Form handling with validation
- **Yup**: Schema validation
- **Recharts**: Data visualization and charts
- **Axios**: HTTP client for API communication
- **React Hot Toast**: User notifications
- **Framer Motion**: Animations and transitions

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment Configuration**
   Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_APP_NAME=Aiqube SMS
   REACT_APP_VERSION=1.0.0
   ```

4. **Start development server**
   ```bash
   npm start
   # or
   yarn start
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── auth/           # Authentication components
│   │   ├── dashboard/      # Dashboard and analytics
│   │   ├── students/       # Student management
│   │   ├── teachers/       # Teacher management
│   │   ├── attendance/     # Attendance system
│   │   ├── fees/          # Fee management
│   │   ├── lms/           # Learning management
│   │   ├── ai/            # AI assistant features
│   │   ├── advanced/      # Advanced features
│   │   ├── reports/       # Reporting and analytics
│   │   ├── settings/      # User settings
│   │   └── layout/        # Layout components
│   ├── contexts/          # React contexts
│   ├── hooks/             # Custom hooks
│   ├── services/          # API services
│   ├── utils/             # Utility functions
│   ├── App.js             # Main app component
│   ├── index.js           # Entry point
│   └── index.css          # Global styles
├── package.json
└── README.md
```

## 🎨 Design System

### Color Palette
- **Primary**: #1976d2 (Blue)
- **Secondary**: #dc004e (Pink)
- **Success**: #4caf50 (Green)
- **Warning**: #ff9800 (Orange)
- **Error**: #f44336 (Red)

### Typography
- **Font Family**: Roboto
- **Weights**: 300, 400, 500, 700

### Responsive Breakpoints
- **Mobile**: < 600px
- **Tablet**: 600px - 960px
- **Desktop**: > 960px

## 🔐 Authentication & Authorization

### User Roles
- **Super Admin**: Full system access
- **Admin**: School-level management
- **Teacher**: Academic management
- **Student**: Student portal access
- **Parent**: Parent portal access

### Protected Routes
- Role-based access control
- Route-level permissions
- Component-level authorization

## 📱 Responsive Design

### Mobile-First Approach
- Touch-friendly interfaces
- Optimized navigation
- Collapsible sidebar
- Responsive data tables
- Mobile-optimized forms

### Progressive Web App Features
- Offline capability
- Push notifications
- App-like experience
- Fast loading times

## 🚀 Performance Optimizations

### Code Splitting
- Route-based code splitting
- Lazy loading of components
- Dynamic imports

### Caching Strategy
- React Query for API caching
- Local storage for user preferences
- Service worker for offline support

### Bundle Optimization
- Tree shaking
- Minification
- Gzip compression
- CDN integration

## 🧪 Testing

### Unit Testing
```bash
npm test
```

### E2E Testing
```bash
npm run test:e2e
```

### Coverage Report
```bash
npm run test:coverage
```

## 📦 Build & Deployment

### Development Build
```bash
npm run build:dev
```

### Production Build
```bash
npm run build
```

### Docker Deployment
```bash
docker build -t aiqube-frontend .
docker run -p 3000:3000 aiqube-frontend
```

## 🔧 Development Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run type-check
```

## 📊 Analytics & Monitoring

### Performance Monitoring
- Core Web Vitals tracking
- Bundle size analysis
- Loading time optimization

### Error Tracking
- Error boundary implementation
- Crash reporting
- User feedback collection

## 🔄 API Integration

### RESTful API
- Axios for HTTP requests
- Request/response interceptors
- Error handling
- Authentication headers

### Real-time Features
- WebSocket connections
- Live notifications
- Real-time updates

## 🎯 Future Enhancements

### Planned Features
- **PWA Support**: Full progressive web app capabilities
- **Offline Mode**: Complete offline functionality
- **Push Notifications**: Real-time notifications
- **Multi-language**: Internationalization support
- **Dark Mode**: Complete dark theme support
- **Accessibility**: WCAG 2.1 compliance
- **Performance**: Advanced optimizations
- **Security**: Enhanced security features

## 🤝 Contributing

### Development Guidelines
1. Follow the existing code style
2. Write meaningful commit messages
3. Add tests for new features
4. Update documentation
5. Follow the Git workflow

### Code Style
- ESLint configuration
- Prettier formatting
- TypeScript for type safety
- Component documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- Check the documentation
- Search existing issues
- Create a new issue
- Contact the development team

### Common Issues
- **Build Errors**: Check Node.js version and dependencies
- **API Errors**: Verify backend is running and accessible
- **Performance Issues**: Check bundle size and optimizations
- **Mobile Issues**: Test responsive design and touch interactions

## 🔗 Related Links

- [Backend Documentation](../README.md)
- [API Documentation](http://localhost:8000/docs)
- [Deployment Guide](../DEPLOYMENT.md)
- [Contributing Guidelines](../CONTRIBUTING.md)