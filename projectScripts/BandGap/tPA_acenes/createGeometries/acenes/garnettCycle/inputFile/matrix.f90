program matrix
  integer:: R,L
  integer:: m,n,k
  real:: mac(4,2),mac2(2,3),mac3(4,3)
  integer::ipiv(4)
   m=4
   n=2
   k=3
  call FILLMATRIX(m,n,mac)
  call FILLMATRIX(n,k,mac2)
  call DGEMM("N","N",m,k,n,1.d0,mac,m,mac2,n,0.d0,mac3,m)

  WRITE(*,*)'Matrix C:'
    DO R=1,m
        do L=1,k
      write(*,*) mac3(R,L)
      enddo
      print*
  end do
    do R=1,m
        do l=1,k
            print*,l 
            mac3(R,L)=l
        enddo
        print*
    enddo
ipiv=(/ 1,3,2,4  /)
!  call dsyswapr('L',m,mac3,k,1,2)
   call slaswp(m,mac3,k,2,4,ipiv,1)
print*,'new matrix C'
  DO R=1,m
        do L=1,k
      write(*,*) mac3(R,L)
      enddo
      print*
  end do
  END program matrix

SUBROUTINE FILLMATRIX (M,N,MATRIX)
   INTEGER M,N
   DOUBLE PRECISION MATRIX(M,N)

    do  I=1,M
    do  J=1,N
      MATRIX(I,J) = I+2*J
    end do
    end do

  WRITE(*,*) 'Matrix:'
    do I=1,M
     write(*,*) (MATRIX(I,J),J=1,N)
    end do

  END
