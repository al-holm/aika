import { Test, TestingModule } from '@nestjs/testing';
import { AuthController } from 'src/auth/auth.controller';
import { AuthService } from 'src/auth/auth.service';
import { Credentials } from 'src/auth/models/credentials';

/**
 * Test suite for the GermanChatController class.
 */
describe('AuthController', () => {
  let controller: AuthController;
  let mockAuthService: Partial<AuthService>;

  beforeEach(async () => {
    // Create a mock service
    mockAuthService = {
      validateCredentials: jest.fn((credentials) =>
        Promise.resolve('cat123'),
      ),
    };

    // Create a module with GermanChatController and the mock service
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AuthController],
      providers: [
        {
          provide: AuthController,
          useValue: mockAuthService,
        },
      ],
    }).compile();

    controller = module.get<AuthController>(AuthController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  /**
   * Describes a test suite for the POST /message endpoint.
   * It tests whether the endpoint returns the processed message correctly.
   * @returns None
   */
  describe('POST /auth', () => {
    it('should return the access token', async () => {
      const credentials = new Credentials;
      credentials.username = 'sss';
      credentials.password = '111';
      credentials.isSignUp = true;

      const response = await controller.authetificate(credentials);

      expect(mockAuthService.validateCredentials).toHaveBeenCalledWith(
        credentials
      );
      expect(response).toEqual({ token: 'cat123' });
    });
});
});
