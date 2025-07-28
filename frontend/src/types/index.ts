// Core types for the application
export interface User {
  id: string
  email: string
  username?: string
  firstName: string
  lastName: string
  role: UserRole
  tenantId?: string
  isEmailVerified: boolean
  profilePicture?: string
  phone?: string
  createdAt: string
  updatedAt?: string
}

export enum UserRole {
  SUPER_ADMIN = 'super_admin',
  ADMIN = 'admin',
  TEACHER = 'teacher',
  STUDENT = 'student',
  PARENT = 'parent',
  STAFF = 'staff',
}

export interface Student {
  id: string
  studentId: string
  admissionNumber: string
  admissionDate: string
  grade: StudentGrade
  currentGrade: StudentGrade
  academicYear: string
  status: StudentStatus
  dateOfBirth: string
  gender: string
  bloodGroup?: string
  nationality?: string
  religion?: string
  motherTongue?: string
  emergencyContact?: string
  emergencyContactRelation?: string
  emergencyContactPhone?: string
  permanentAddress?: string
  currentAddress?: string
  city?: string
  state?: string
  country?: string
  postalCode?: string
  previousSchool?: string
  previousGrade?: string
  medicalConditions?: string
  allergies?: string
  medications?: string
  emergencyMedicalInfo?: string
  usesTransport: boolean
  transportRoute?: string
  pickupLocation?: string
  dropLocation?: string
  usesHostel: boolean
  hostelRoom?: string
  hostelBlock?: string
  cgpa: number
  totalCredits: number
  attendancePercentage: number
  userId: string
  tenantId: string
  createdAt: string
  updatedAt?: string
}

export enum StudentGrade {
  KINDERGARTEN = 'kindergarten',
  GRADE_1 = 'grade_1',
  GRADE_2 = 'grade_2',
  GRADE_3 = 'grade_3',
  GRADE_4 = 'grade_4',
  GRADE_5 = 'grade_5',
  GRADE_6 = 'grade_6',
  GRADE_7 = 'grade_7',
  GRADE_8 = 'grade_8',
  GRADE_9 = 'grade_9',
  GRADE_10 = 'grade_10',
  GRADE_11 = 'grade_11',
  GRADE_12 = 'grade_12',
  UNIVERSITY = 'university',
}

export enum StudentStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  GRADUATED = 'graduated',
  TRANSFERRED = 'transferred',
  SUSPENDED = 'suspended',
}

export interface Teacher {
  id: string
  teacherId: string
  employeeId: string
  joiningDate: string
  department?: string
  designation?: string
  qualification?: TeacherQualification
  specialization?: string
  experienceYears: number
  status: TeacherStatus
  dateOfBirth: string
  gender: string
  bloodGroup?: string
  nationality?: string
  emergencyContact?: string
  emergencyContactRelation?: string
  emergencyContactPhone?: string
  permanentAddress?: string
  currentAddress?: string
  city?: string
  state?: string
  country?: string
  postalCode?: string
  employmentType?: string
  salary?: number
  bankName?: string
  bankAccountNumber?: string
  ifscCode?: string
  previousInstitution?: string
  previousDesignation?: string
  experienceDetails?: string
  medicalConditions?: string
  allergies?: string
  emergencyMedicalInfo?: string
  usesTransport: boolean
  transportRoute?: string
  pickupLocation?: string
  dropLocation?: string
  usesHostel: boolean
  hostelRoom?: string
  hostelBlock?: string
  performanceRating: number
  attendancePercentage: number
  studentSatisfaction: number
  profilePicture?: string
  resume?: string
  certificates?: string
  medicalCertificate?: string
  userId: string
  tenantId: string
  createdAt: string
  updatedAt?: string
}

export enum TeacherQualification {
  BACHELORS = 'bachelors',
  MASTERS = 'masters',
  PHD = 'phd',
  DIPLOMA = 'diploma',
  CERTIFICATION = 'certification',
  OTHER = 'other',
}

export enum TeacherStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ON_LEAVE = 'on_leave',
  TERMINATED = 'terminated',
  RETIRED = 'retired',
}

export interface AttendanceRecord {
  id: string
  tenantId: string
  userId: string
  studentId?: string
  teacherId?: string
  classId?: string
  date: string
  timeIn?: string
  timeOut?: string
  status: AttendanceStatus
  method: AttendanceMethod
  latitude?: number
  longitude?: number
  locationAddress?: string
  locationAccuracy?: number
  qrCodeId?: string
  qrScanTime?: string
  markedBy?: string
  remarks?: string
  isVerified: boolean
  verifiedBy?: string
  verificationTime?: string
  createdAt: string
  updatedAt?: string
}

export enum AttendanceStatus {
  PRESENT = 'present',
  ABSENT = 'absent',
  LATE = 'late',
  HALF_DAY = 'half_day',
  LEAVE = 'leave',
  HOLIDAY = 'holiday',
}

export enum AttendanceMethod {
  MANUAL = 'manual',
  QR_CODE = 'qr_code',
  GEOLOCATION = 'geolocation',
  BIOMETRIC = 'biometric',
  RFID = 'rfid',
}

export interface FeeRecord {
  id: string
  tenantId: string
  studentId: string
  feeType: FeeType
  academicYear: string
  semester?: string
  month?: string
  totalAmount: number
  paidAmount: number
  discountAmount: number
  lateFee: number
  dueDate: string
  gracePeriodDays: number
  status: PaymentStatus
  isWaived: boolean
  waiverReason?: string
  description?: string
  remarks?: string
  createdAt: string
  updatedAt?: string
}

export enum FeeType {
  TUITION = 'tuition',
  TRANSPORT = 'transport',
  HOSTEL = 'hostel',
  LIBRARY = 'library',
  LABORATORY = 'laboratory',
  SPORTS = 'sports',
  EXAMINATION = 'examination',
  MISCELLANEOUS = 'miscellaneous',
  UNIFORM = 'uniform',
  BOOKS = 'books',
  MEALS = 'meals',
  ACTIVITIES = 'activities',
}

export enum PaymentStatus {
  PENDING = 'pending',
  PAID = 'paid',
  PARTIAL = 'partial',
  OVERDUE = 'overdue',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded',
}

export interface Payment {
  id: string
  feeRecordId: string
  tenantId: string
  paymentId: string
  amount: number
  paymentMethod: PaymentMethod
  paymentDate: string
  transactionId?: string
  referenceNumber?: string
  bankName?: string
  chequeNumber?: string
  status: PaymentStatus
  isVerified: boolean
  verifiedBy?: string
  verificationTime?: string
  remarks?: string
  receiptUrl?: string
  createdAt: string
  updatedAt?: string
}

export enum PaymentMethod {
  CASH = 'cash',
  BANK_TRANSFER = 'bank_transfer',
  CHEQUE = 'cheque',
  CREDIT_CARD = 'credit_card',
  DEBIT_CARD = 'debit_card',
  ONLINE_PAYMENT = 'online_payment',
  MOBILE_PAYMENT = 'mobile_payment',
  SCHOLARSHIP = 'scholarship',
  WAIVER = 'waiver',
}

// AI Assistant types
export interface AIAssistant {
  id: number
  name: string
  description?: string
  modelType: string
  subjectCategory: string
  isActive: boolean
  maxTokens: number
  temperature: number
  systemPrompt?: string
  customInstructions?: string
  rateLimitPerMinute: number
  costPerToken: number
  createdAt: string
  updatedAt: string
}

export interface AIConversation {
  id: number
  subject: string
  topic?: string
  status: string
  totalTokensUsed: number
  totalCost: number
  startedAt: string
  endedAt?: string
  createdAt: string
  updatedAt: string
  assistant: AIAssistant
  studentName: string
  teacherName?: string
}

export interface AIMessage {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  tokensUsed: number
  cost: number
  responseTimeMs?: number
  modelUsed?: string
  confidenceScore?: number
  feedbackRating?: number
  feedbackComment?: string
  createdAt: string
}

// Dashboard types
export interface DashboardStats {
  totalStudents: number
  newStudentsThisMonth: number
  totalTeachers: number
  attendanceStats: {
    totalRecords: number
    presentCount: number
    attendanceRate: number
  }
  feeStats: {
    totalFees: number
    collectedAmount: number
    collectionRate: number
  }
  academicStats: {
    totalStudents: number
    avgAttendance: number
  }
  recentActivities: Array<{
    type: string
    description: string
    timestamp: string
    status: string
  }>
  alerts: Array<{
    type: string
    title: string
    message: string
    count: number
  }>
}

// API Response types
export interface ApiResponse<T = any> {
  data?: T
  message?: string
  error?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// Form types
export interface LoginForm {
  email: string
  password: string
}

export interface StudentForm {
  email: string
  username?: string
  password: string
  firstName: string
  lastName: string
  phone?: string
  studentId: string
  admissionNumber: string
  admissionDate: string
  grade: StudentGrade
  academicYear: string
  dateOfBirth: string
  gender: string
  bloodGroup?: string
  nationality?: string
  religion?: string
  motherTongue?: string
  emergencyContact?: string
  emergencyContactRelation?: string
  emergencyContactPhone?: string
  permanentAddress?: string
  currentAddress?: string
  city?: string
  state?: string
  country?: string
  postalCode?: string
  previousSchool?: string
  previousGrade?: string
  medicalConditions?: string
  allergies?: string
  medications?: string
  emergencyMedicalInfo?: string
  usesTransport: boolean
  transportRoute?: string
  pickupLocation?: string
  dropLocation?: string
  usesHostel: boolean
  hostelRoom?: string
  hostelBlock?: string
}

export interface TeacherForm {
  email: string
  username: string
  password: string
  confirmPassword: string
  firstName: string
  lastName: string
  employeeId: string
  dateOfBirth: string
  gender: string
  phone: string
  address: string
  city: string
  state: string
  country: string
  postalCode: string
  qualification: TeacherQualification
  specialization: string
  hireDate: string
  salary?: number
  emergencyContactName: string
  emergencyContactPhone: string
  emergencyContactRelationship: string
  medicalConditions?: string
  allergies?: string
  bloodGroup?: string
  transportRequired: boolean
  transportRoute?: string
  hostelRequired: boolean
  hostelRoom?: string
  experienceYears?: number
  experienceDetails?: any
  certificates?: any
  bio?: string
  profilePicture?: string
}

// Theme types
export type Theme = 'light' | 'dark' | 'system'

// Navigation types
export interface NavItem {
  title: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  badge?: string | number
  children?: NavItem[]
}

// Chart data types
export interface ChartData {
  labels: string[]
  datasets: Array<{
    label: string
    data: number[]
    backgroundColor?: string | string[]
    borderColor?: string | string[]
    borderWidth?: number
  }>
}

// Filter types
export interface StudentFilter {
  search?: string
  grade?: StudentGrade
  status?: StudentStatus
  page?: number
  limit?: number
}

export interface TeacherFilter {
  search?: string
  department?: string
  qualification?: TeacherQualification
  status?: TeacherStatus
  page?: number
  limit?: number
}

export interface AttendanceFilter {
  studentId?: string
  teacherId?: string
  dateFrom?: string
  dateTo?: string
  status?: AttendanceStatus
  method?: AttendanceMethod
  page?: number
  limit?: number
}

export interface FeeFilter {
  studentId?: string
  feeType?: FeeType
  academicYear?: string
  semester?: string
  status?: PaymentStatus
  dueDateFrom?: string
  dueDateTo?: string
  amountMin?: number
  amountMax?: number
  page?: number
  limit?: number
}

// Notification types
export interface Notification {
  id: string
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  read: boolean
  createdAt: string
  actionUrl?: string
}

// Settings types
export interface UserSettings {
  theme: Theme
  language: string
  timezone: string
  notifications: {
    email: boolean
    sms: boolean
    push: boolean
    attendanceAlerts: boolean
    feeReminders: boolean
    gradeUpdates: boolean
    assignmentDeadlines: boolean
  }
}

// Error types
export interface ApiError {
  message: string
  code?: string
  details?: any
}

// File upload types
export interface FileUpload {
  file: File
  progress: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  url?: string
  error?: string
}

// Advanced features types
export interface BlockchainCertificate {
  id: string
  studentId: string
  certificateType: string
  title: string
  description?: string
  issuerName: string
  blockchainHash?: string
  blockchainNetwork: string
  status: 'pending' | 'issued' | 'verified' | 'revoked'
  issuedDate: string
  expiryDate?: string
  verificationUrl?: string
  createdAt: string
  updatedAt: string
}

export interface IoTDevice {
  id: string
  deviceId: string
  deviceType: string
  name: string
  location?: string
  building?: string
  room?: string
  status: string
  lastSeen?: string
  isOnline: boolean
  batteryLevel?: number
  createdAt: string
  updatedAt: string
}

export interface GamificationBadge {
  id: string
  badgeType: string
  name: string
  description?: string
  iconUrl?: string
  pointsValue: number
  rarity: string
  isActive: boolean
  createdAt: string
  updatedAt: string
}

// Utility types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}